import logging

from service.kuberesource import KubeResource

logger = logging.getLogger(__name__)


class EndpointsResource(KubeResource):

    RESOURCE_TYPE = 'endpoints'
