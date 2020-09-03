import logging

from service.kuberesource import KubeResource

logger = logging.getLogger(__name__)


class StatefulSetResource(KubeResource):

    RESOURCE_TYPE = 'statefulset'
