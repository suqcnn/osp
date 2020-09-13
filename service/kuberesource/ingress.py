import logging

from service.kuberesource import KubeResource

logger = logging.getLogger(__name__)


class IngressResource(KubeResource):

    RESOURCE_TYPE = 'ingress'
