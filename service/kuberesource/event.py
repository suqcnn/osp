import logging

from service.kuberesource import KubeResource

logger = logging.getLogger(__name__)


class EventResource(KubeResource):

    RESOURCE_TYPE = 'event'
