import logging

from service.kuberesource import KubeResource

logger = logging.getLogger(__name__)


class NamespaceResource(KubeResource):

    RESOURCE_TYPE = 'namespace'
