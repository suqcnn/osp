import logging

from service.kuberesource import KubeResource

logger = logging.getLogger(__name__)


class CronJobResource(KubeResource):

    RESOURCE_TYPE = 'cronjob'
