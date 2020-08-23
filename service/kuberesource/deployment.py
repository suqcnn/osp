import logging

from service.kuberesource import KubeResource

logger = logging.getLogger(__name__)


class DeploymentResource(KubeResource):

    RESOURCE_TYPE = 'deployment'
