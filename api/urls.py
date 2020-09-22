from api import SlashOptionRouter
from api.views import user, cluster, pod, namespace, node, event, deployment, config_map, statefulset, \
     daemonset, job, cronjob, persistent_volume, persistent_volume_claim, storage_class, service, ingress, \
     endpoints, networkpolicy, serviceaccount, rolebinding, role

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
router.register('persistent_volume_claim/(?P<cluster>[^/.]+)',
                persistent_volume_claim.PersistentVolumeClaimViewSet,
                basename='pvc')
router.register('storage_class/(?P<cluster>[^/.]+)', storage_class.StorageClassViewSet, basename='storage class')
router.register('service/(?P<cluster>[^/.]+)', service.ServiceViewSet, basename='service')
router.register('ingress/(?P<cluster>[^/.]+)', ingress.IngressViewSet, basename='ingress')
router.register('endpoints/(?P<cluster>[^/.]+)', endpoints.EndpointsViewSet, basename='endpoints')
router.register('networkpolicy/(?P<cluster>[^/.]+)', networkpolicy.NetworkPolicyViewSet, basename='networkpolicy')
router.register('serviceaccount/(?P<cluster>[^/.]+)', serviceaccount.ServiceAccountViewSet, basename='serviceaccount')
router.register('rolebinding/(?P<cluster>[^/.]+)', rolebinding.RoleBindingViewSet, basename='rolebinding')
router.register('role/(?P<cluster>[^/.]+)', role.RoleViewSet, basename='role')

urlpatterns = router.urls
