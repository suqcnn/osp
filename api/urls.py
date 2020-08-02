from api import SlashOptionRouter
from api.views import user, cluster, pod, namespace

router = SlashOptionRouter()

router.register('user', user.UserViewSet, basename='user')
router.register('cluster', cluster.ClusterViewSet, basename='cluster')
router.register('pods/(?P<cluster>[^/.]+)', pod.PodViewSet, basename='pod')
router.register('namespace/(?P<cluster>[^/.]+)', namespace.NamespaceViewSet, basename='namespace')

urlpatterns = router.urls
