from api import SlashOptionRouter
from api.views import user, cluster, pod, namespace, node, event, deployment, config_map, statefulset, \
     daemonset, job, cronjob, persistent_volume

router = SlashOptionRouter()

router.register('user', user.UserViewSet, basename='user')
router.register('cluster', cluster.ClusterViewSet, basename='cluster')
router.register('pods/(?P<cluster>[^/.]+)', pod.PodViewSet, basename='pod')
router.register('nodes/(?P<cluster>[^/.]+)', node.NodeViewSet, basename='node')
router.register('namespace/(?P<cluster>[^/.]+)', namespace.NamespaceViewSet, basename='namespace')
router.register('event/(?P<cluster>[^/.]+)', event.EventViewSet, basename='event')
router.register('deployment/(?P<cluster>[^/.]+)', deployment.DeploymentViewSet, basename='deployment')
router.register('config_map/(?P<cluster>[^/.]+)', config_map.ConfigMapViewSet, basename='config_map')
router.register('statefulset/(?P<cluster>[^/.]+)', statefulset.StatefulSetViewSet, basename='statefulset')
router.register('daemonset/(?P<cluster>[^/.]+)', daemonset.DaemonSetViewSet, basename='daemonset')
router.register('job/(?P<cluster>[^/.]+)', job.JobViewSet, basename='job')
router.register('cronjob/(?P<cluster>[^/.]+)', cronjob.CronJobViewSet, basename='cronjob')
router.register('persistent_volume/(?P<cluster>[^/.]+)', persistent_volume.PersistentVolumeViewSet, basename='pv')

urlpatterns = router.urls
