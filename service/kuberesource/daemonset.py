import logging

from service.kuberesource import KubeResource

logger = logging.getLogger(__name__)


class DaemonSetResource(KubeResource):

    RESOURCE_TYPE = 'daemonset'
