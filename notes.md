# Samsung:
docker network create -d macvlan  \
    --subnet=10.100.0.0/24  \
    --ip-range=10.100.0.16/28 \
    --gateway=10.100.0.1  \
    -o parent=enp2s0.100 test100
docker network create -d macvlan  \
    --subnet=10.120.0.0/24  \
    --ip-range=10.120.0.16/28 \
    --gateway=10.120.0.1  \
    -o parent=enp2s0.120 test120
docker network create -d macvlan  \
    --subnet=10.130.0.0/24  \
    --ip-range=10.130.0.16/28 \
    --gateway=10.130.0.1  \
    -o parent=enp2s0.130 test130
docker network create -d macvlan  \
    --subnet=10.140.0.0/24  \
    --ip-range=10.140.0.16/28 \
    --gateway=10.140.0.1  \
    -o parent=enp2s0.140 test140

 macvlan ima problem - zahteva *.vlan_id v parent parametru! Ni ok za Mac testing environment

 v tem primeru se je treba poslužiti bridge načina!

brctl addbr br140
brctl addif br140 enp2s0.140
docker network create -d bridge \
	--subnet=10.140.0.0/24  \
    --ip-range=10.140.0.32/28 \
    --gateway=10.140.0.1  \
    -o parent=enp2s0.140 test140

brctl addbr br130
brctl addif br130 enp2s0.130
docker network create -d bridge \
	--subnet=10.130.0.0/24  \
    --ip-range=10.130.0.32/28 \
    --gateway=10.130.0.1  \
    -o parent=enp2s0.130 test130

docker run -itd --net test130 --name c130 centos:7
docker run -itd --net test140 --name c140 centos:7

### Expermiental DHCP IPAM driver - for usage special docker image 
https://docker-py.readthedocs.io/en/stable/
http://blog.oddbit.com/2014/08/11/four-ways-to-connect-a-docker/
https://github.com/docker/libnetwork/issues/843
https://github.com/nerdalert/libnetwork/tree/dhcp_client
Expermiental: https://gist.github.com/nerdalert/3d2b891d41e0fa8d688c
docker network create -d macvlan \
  --ipam-driver=dhcp \
  -o parent=enp2s0.120 \
  --ipam-opt dhcp_interface=enp2s0.120 test120








# Trusty:
docker network create -d macvlan  \
    --subnet=10.100.0.0/24  \
    --ip-range=10.100.0.32/28 \
    --gateway=10.100.0.1  \
    -o parent=vlan0 test100
docker network create -d macvlan  \
    --subnet=10.200.0.0/24  \
    --ip-range=10.200.0.23/28 \
    --gateway=10.200.0.1  \
    -o parent=vlan1 test200