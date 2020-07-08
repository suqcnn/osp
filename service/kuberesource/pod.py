import logging

from service.kuberesource import KubeResource

logger = logging.getLogger(__name__)


class PodResource(KubeResource):

    RESOURCE_TYPE = 'pod'
