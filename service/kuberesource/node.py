import logging

from service.kuberesource import KubeResource

logger = logging.getLogger(__name__)


class NodeResource(KubeResource):

    RESOURCE_TYPE = 'node'
