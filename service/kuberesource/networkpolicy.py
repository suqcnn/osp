import logging

from service.kuberesource import KubeResource

logger = logging.getLogger(__name__)


class NetworkPolicyResource(KubeResource):

    RESOURCE_TYPE = 'networkpolicy'
