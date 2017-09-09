import os
import json
import docker
import ipaddress
from api.client import APIClient


class NUTRegistrator:

    api = None
    api_url = None
    api_path = None
    api_token = None
    docker_client = None
    node_info = None
    node_networks = None
    node_containers = None
    schema = None

    def __init__(self, api_url, api_path, api_token):
        """
        Class for registration of node dokcer information no NUT server.
        """
        self.api_url = api_url
        self.api_path = api_path
        self.api_token = api_token

    def authenticate(self):
        """
        Authenticate against NUT server API
        """
        self.api = APIClient(
            api_url=self.api_url,
            api_path=self.api_path,
            api_token=self.api_token
        )
        self.schema = self.api.get(path=self.api.url)

    def get_docker_environment(self):
        """
        Return docker environment.
        """
        self.docker_client = docker.from_env()
        return self.docker_client

    def get_node_info(self):
        """
        Return basic information about docker host from docker service.
        """
        # Check for docker environment
        if not self.docker_client:
            self.get_docker_environment()

        info = self.docker_client.info()
        hostname = os.uname()[1]
        payload = {
            'hostname': info["Name"],
            'running_containers': info['ContainersRunning'],
            'containers': info['Containers'],
            'hostname_host': hostname,
            'active': True
        }
        self.node_info = payload
        return self.node_info

    def get_node_networks(self):
        """
        Return dokcer networks information
        """
        # Check for docker environment
        if not self.docker_client:
            self.get_docker_environment()

        network_list = filter(lambda network: network.name != "none",
                              self.docker_client.networks.list())
        self.node_networks = [
            {
                'name': i.attrs["Name"],
                'network_id': i.attrs["Id"],
                'active': True,
                'subnet': i.attrs['IPAM']
            }
            for i in network_list]
        return self.node_networks

    def get_node_containers(self):
        """
        Return docker containers information
        """
        # Check for docker environment
        if not self.docker_client:
            self.get_docker_environment()

        containers = self.docker_client.containers.list(all=True)
        self.node_containers = [c.__dict__ for c in containers]
        return self.node_containers

    def list_dicts_to_dict_dicts(self, list_dicts, key):
        """
        Return dict of dicts with key as index
        """
        return {element[key]: element for element in list_dicts}

    def register_node(self, include_networks=False):
        """
        Register node docker information to NUT server REST API.

        include_networks: Include netwokrs with registration.
        """
        # Initiate API Client
        if not self.api:
            self.authenticate()
        # Retreive data from docker host
        if not self.node_info:
            self.get_node_info()

        # Register node to NUT server
        hostname = self.node_info['hostname']
        nodes = self.api.get("%s?hostname=%s" %
                             (self.schema['nodes'], hostname))
        if nodes["count"] == 0:
            node = self.api.post("nodes/", payload=payload)
        elif nodes["count"] == 1:
            node = nodes["results"][0]
            if int(node["running_containers"]) != \
                self.node_info["running_containers"] or \
               int(node["containers"]) != self.node_info["containers"] or \
               not node["active"]:
                node = api.put(
                    "%s%s/" % (self.schema['nodes'], node["id"]),
                    payload=self.node_info
                )
        else:
            raise Exception("More than one node with hostname %s found; %s" % (
                hostname, nodes))
        if include_networks:
            self.register_networks(node=node["id"])
        return hostname

    def register_networks(self, node):
        """
        Register node netwokrs against NUT server

        node: NUT API node id for referencing network to node
        """
        # Initiate API Client
        if not self.api:
            self.authenticate()
        # Retreive data from docker host
        if not self.node_networks:
            self.get_node_networks()

        # Get node networks
        networks = self.api.get("%s?node=%s" %
                                (self.schema['networks'], node))
        networks = networks['results']
        api_networks = self.list_dicts_to_dict_dicts(networks, "network_id")
        node_networks = self.list_dicts_to_dict_dicts(
            self.node_networks, "network_id")

        # register new networks
        for network_id in list(set(node_networks.keys()) -
                               set(api_networks.keys())):
            print("Register network: %s" % network_id)
            node_networks[network_id]['node'] = node
            network = self.api.post(
                self.schema['networks'],
                node_networks[network_id]
            )
            self._register_subnets(
                network['id'],
                node_networks[network_id]
            )
        # update information on registered networks
        for network_id in list(
            set(api_networks.keys()).intersection(set(node_networks.keys()))
        ):
            n_info_keys = list(
                set(api_networks[network_id].keys()).intersection(
                    set(node_networks[network_id].keys())))
            # compare network information and generate True/False list
            node_match_tf_list = [
                api_networks[network_id][key] == node_networks[network_id][key]
                for key in n_info_keys
            ]
            if not all(node_match_tf_list):  # Update Network
                print("Update network: %s" % network_id)
                payload = api_networks[network_id]
                for key in node_networks[network_id].keys():
                    payload[key] = node_networks[network_id][key]
                self.api.put(
                    "%s%s/" % (self.schema['networks'], payload["id"]),
                    payload
                )
            self._register_subnets(
                api_networks[network_id]['id'],
                node_networks[network_id]
            )
        # deactivate abandoned networks
        for network_id in list(set(api_networks.keys()) -
                               set(node_networks.keys())):
            # Update Network active flag to False
            if api_networks[network_id]["active"]:
                print("Deactivate: %s" % network_id)
                self.api.patch(
                    "%s%s/" % (self.schema['networks'],
                               api_networks[network_id]["id"]),
                    {'active': False}
                )

    def subnet_to_api_subnet(self, subnet):
        subnet_api = {
            #"network": None,
            "active": True,
            "ipv6_subnet_ip": None,
            "ipv6_subnet_mask": 64,
            "ipv6_gateway": None,
            "ipv4_subnet_ip": None,
            "ipv4_subnet_mask": 16,
            "ipv4_gateway": None,
            #"ipv6": True
        }
        ipv6 = True
        try:
            ip_address = ipaddress.IPv6Network(subnet["Subnet"])
            ip_gateway = ipaddress.IPv6Address(subnet["Gateway"])
        except ipaddress.AddressValueError:
            ip_address = ipaddress.IPv4Network(subnet["Subnet"])
            ip_gateway = ipaddress.IPv4Address(subnet["Gateway"])
            ipv6 = False
        #subnet_api['ipv6'] = ipv6
        if ipv6:
            subnet_api['ipv6_subnet_ip'] = str(ip_address.network_address)
            subnet_api['ipv6_subnet_mask'] = int(ip_address.prefixlen)
            subnet_api['ipv6_gateway'] = str(ip_gateway.address)
        else:
            subnet_api['ipv4_subnet_ip'] = str(ip_address.network_address)
            subnet_api['ipv4_subnet_mask'] = int(ip_address.prefixlen)
            subnet_api['ipv4_gateway'] = str(ip_gateway.compressed)
        return subnet_api

    def _register_subnets(self, network_api_id, node_network):
        """
        Register subnet for network

        network_api_id: ID on networks API endpoint
        node_network: network information dict containing 'subnet' key
        """
        # Initiate API Client
        if not self.api:
            self.authenticate()

        # Get network subnets
        api_subnets = self.api.get("%s?network=%s" %
                                   (self.schema['subnets'], network_api_id))
        if api_subnets['previous'] or api_subnets['next']:
            raise Exception("Not implemented error: Pagination enabled API \
                returned multiple pages for network %s: %s" % (api_subnets,
                                                               network_api_id))
        api_subnets = api_subnets['results']
        # print "api_subnets %s" % json.dumps(api_subnets)
        network_subnets = [
            self.subnet_to_api_subnet(s)
            for s in node_network["subnet"]["Config"]
        ]
        # print "network_subnet %s" % json.dumps(network_subnets)

        # compare all subnets
        reviewed_subnets = []
        reviewed_api_subnets = []
        for i, network_subnet in enumerate(network_subnets):
            for j, api_subnet in enumerate(api_subnets):
                network_comparison = [
                    network_subnet[ns_key] == api_subnet[ns_key]
                    for ns_key in network_subnet.keys()
                ]
                if all(network_comparison):
                    reviewed_subnets.append(i)
                    reviewed_api_subnets.append(j)
                    break
        # list not registered or obsolite subnets
        not_reviewed_subnets = [i
                                for i in range(len(network_subnets))
                                if i not in reviewed_subnets]
        not_reviewed_api_subnets = [j
                                    for j in range(len(api_subnets))
                                    if j not in reviewed_api_subnets]

        # Print debug status
        # print "Subnets to keep %d, subnets to add: %d, subnets to delete %d" \
        #    % (
        #    len(reviewed_subnets),
        #    len(not_reviewed_subnets),
        #    len(not_reviewed_api_subnets)
        #)

        # Make API calls
        for i in not_reviewed_subnets:
            payload = network_subnets[i]
            payload['network'] = network_api_id
            self.api.post("%s" % self.schema['subnets'], payload)
        for i in not_reviewed_api_subnets:
            sid = api_subnets[i]['id']
            self.api.delete("%s%s/" % (self.schema['subnets'], sid))
