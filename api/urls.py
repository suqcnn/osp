from api import SlashOptionRouter
from api.views import user, cluster, pod

router = SlashOptionRouter()

router.register('user', user.UserViewSet, basename='user')
router.register('cluster', cluster.ClusterViewSet, basename='cluster')
router.register('pod', pod.PodViewSet, basename='pod')

urlpatterns = router.urls
