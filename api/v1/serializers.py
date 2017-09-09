from nodes.models import Node, Container, Network, Subnet
from rest_framework import serializers, viewsets
from django_filters.rest_framework import DjangoFilterBackend


class NodeSerializer(serializers.ModelSerializer):
        # Serializers define the API representation.
    id = serializers.ReadOnlyField()

    class Meta:
        model = Node
        fields = '__all__'


class NodeViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        Return a node instance.

    list:
        Return all nodes.

    create:
        Create a new node.

    delete:
        Remove an existing node.

    partial_update:
        Update one or more fields on an existing node.

    update:
        Update a node.
    """

    queryset = Node.objects.all() 
    serializer_class = NodeSerializer
    filter_fields = ('hostname',)


class ContainerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Container
        fields = '__all__'


class ContainerViewSet(viewsets.ModelViewSet):
    queryset = Container.objects.all()
    serializer_class = ContainerSerializer
    filter_fields = ('node', 'container_id', 'container_name')


class NetworkSerializer(serializers.ModelSerializer):

    class Meta:
        model = Network
        fields = '__all__'


class NetworkViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        Return docker network

    list:
        Return all registered networks.

    create:
        Create a new docker network on node.

    delete:
        Remove an existing docker network.

    partial_update:
        Update one or more fields on an existing docker network.

    update:
        Update a docker network.
    """
    queryset = Network.objects.all()
    serializer_class = NetworkSerializer
    filter_fields = ('node', 'name', 'network_id')


class SubnetSerializer(serializers.ModelSerializer):
    #network = NetworkSerializer()

    class Meta:
        model = Subnet
        fields = '__all__'


class SubnetViewSet(viewsets.ModelViewSet):
    queryset = Subnet.objects.all()
    serializer_class = SubnetSerializer
    filter_fields = ('network', 'ipv4_subnet_ip', 'ipv6_subnet_ip')
