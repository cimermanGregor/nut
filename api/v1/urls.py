from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.authtoken import views
from rest_framework.schemas import get_schema_view
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer
from api.v1.serializers import NodeViewSet, ContainerViewSet, NetworkViewSet, SubnetViewSet

# Routers provide an easy way of automatically determining the URL conf.
router_nodes = routers.DefaultRouter()
router_nodes.register(r'nodes', NodeViewSet)
router_nodes.register(r'containers', ContainerViewSet)
router_nodes.register(r'networks', NetworkViewSet)
router_nodes.register(r'subnets', SubnetViewSet)

schema_view = get_schema_view(
    title='Network Unit Test API',
    renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer]
)

urlpatterns = [
	url(r'^api-token-auth/', views.obtain_auth_token),
	url(r'^swagger', schema_view),
    url(r'^', include(router_nodes.urls)),
]

#urlpatterns = format_suffix_patterns(urlpatterns)


