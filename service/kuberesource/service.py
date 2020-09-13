import logging

from service.kuberesource import KubeResource

logger = logging.getLogger(__name__)


class ServiceResource(KubeResource):

    RESOURCE_TYPE = 'service'
