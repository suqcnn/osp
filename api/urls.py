from api import SlashOptionRouter
from api.views import user, cluster, pod, namespace, node, event, deployment

router = SlashOptionRouter()

router.register('user', user.UserViewSet, basename='user')
router.register('cluster', cluster.ClusterViewSet, basename='cluster')
router.register('pods/(?P<cluster>[^/.]+)', pod.PodViewSet, basename='pod')
router.register('nodes/(?P<cluster>[^/.]+)', node.NodeViewSet, basename='node')
router.register('namespace/(?P<cluster>[^/.]+)', namespace.NamespaceViewSet, basename='namespace')
router.register('event/(?P<cluster>[^/.]+)', event.EventViewSet, basename='event')
router.register('deployment/(?P<cluster>[^/.]+)', deployment.DeploymentViewSet, basename='deployment')

urlpatterns = router.urls
