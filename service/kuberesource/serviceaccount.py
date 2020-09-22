import logging

from service.kuberesource import KubeResource

logger = logging.getLogger(__name__)


class ServiceAccountResource(KubeResource):

    RESOURCE_TYPE = 'serviceaccount'
