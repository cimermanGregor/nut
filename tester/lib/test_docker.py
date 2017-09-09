import requests
import docker
import json
import time
import os
import slumber
from requests.auth import AuthBase

DOCKER_IMAGE = "centos:7"
DOCKER_COMMAND = "/bin/sh -c 'for i in {0..9}; do echo $i; sleep 1; done'"
API_TOKEN = "596b81179a86b686cf531d926e80be593bba0f06"

class ParseAuth(AuthBase):
    def __init__(self, api_header, api_key):
        self.api_header = api_header
        self.api_key = api_key

    def __call__(self, r):
        r.headers[self.api_header] = self.api_key
        return r

class ApiClient():

    def __init__(self, api_url="http://0.0.0.0:8000", api_base_path="api/v1", api_token=None, username=None, password=None):
        url = "%s/%s" % (api_url, api_base_path)
        if api_token:
            self.headers = {'Authorization': "Token %s" % api_token, 'WWW-Authenticate': 'Token'}
        else:
            r = requests.get(url, auth=(username, password))
            #Token
        self.url = url
        self.token = api_token

    def get(self, path="/"):
        print("%s/%s Headers: %s" % (self.url, path, self.headers))
        response = requests.get("%s/%s" % (self.url, path), headers=self.headers)
        if response.status_code in [200]:
            return response
        else:
            raise Exception(response)


def run_test_container(client):
    container = client.containers.run(
        DOCKER_IMAGE, DOCKER_COMMAND, detach=True)

    print container

    # for line in container.logs(stream=True):
    #   print line.strip()

    print container.status
    time.sleep(12)
    print container.status
    # if container.
    print container.kill()
    print container.logs()
    print container.status

def get_docker_environemnt():
    return docker.from_env()

def extract_node_info(client):
    info = client.info()
    hostname = os.uname()[1]
    payload = {
        'hostname': info["Name"],
        'running_containers': info['ContainersRunning'],
        'containers': info['Containers'],
        'hostname_2': hostname,
        'active': True
    }
    return payload


def extract_networks(client):
    networks_list = filter(lambda network: network.name != "none",
                           client.networks.list())
    return [i.attrs for i in networks_list]


def extract_containers(client):
    containers = client.containers.list(all=True)
    return [c.__dict__ for c in containers]

def register_node(payload, api_token):
    """
    Registers node to REST API based on received payload extraced from 
    docker command.
    """
    
    
    nodes = api.get("nodes/?hostname=%s" % payload['hostname'])
    if nodes["count"] == 0:
        node = api.post("nodes/", payload=payload)
    elif nodes["count"] == 1:
        node = nodes["results"][0]
        if int(node["running_containers"]) != payload["running_containers"] or int(node["containers"]) != payload["containers"] or not node["active"]:
            node = api.put("nodes/%s/" % node["id"], payload=payload)
    else:
        raise Exception("More than one node with hostname %s found; %s" %(payload["hostname"], nodes))
    print node
    return node['id']

def register_networks(payload, node_id, api_token):
    """
    Registers network to NUT API using payload
    """
    from api.client import APIClient
    api = APIClient(api_token=api_token)
    #nodes = api.get("nodes/?hostname=%s" % payload['hostname'])
    


#if __name__ == '__main__':
#    client = docker.from_env()
#    # run_test_container(client)
#    # print(extract_networks(client))
#    # print(extract_containers(client))
#    payload = extract_node_info(client)
#    nodes = register_node(payload)
#    #print(json.dumps(nodes['results'], indent=2))




