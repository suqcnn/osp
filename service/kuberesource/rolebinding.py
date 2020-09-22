import logging

from service.kuberesource import KubeResource

logger = logging.getLogger(__name__)


class RoleBindingResource(KubeResource):

    RESOURCE_TYPE = 'rolebinding'
