import logging

from service.kuberesource import KubeResource

logger = logging.getLogger(__name__)


class JobResource(KubeResource):

    RESOURCE_TYPE = 'job'
