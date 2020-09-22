import logging

from service.kuberesource import KubeResource

logger = logging.getLogger(__name__)


class RoleResource(KubeResource):

    RESOURCE_TYPE = 'role'
