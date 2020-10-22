import logging

from service.kuberesource import KubeResource

logger = logging.getLogger(__name__)


class ClusterResource(KubeResource):

    RESOURCE_TYPE = 'cluster'
