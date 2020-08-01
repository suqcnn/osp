import logging

from service.kuberesource import KubeResource
from utils import CommonReturn, Code

logger = logging.getLogger(__name__)


class WatchResource(KubeResource):

    RESOURCE_TYPE = 'watch'

    def close_watch(self):
        has_watch_client = self.middle_message.has_watch_client(self.cluster)
        if not has_watch_client:
            return self.get({'action': 'close'})
        return CommonReturn(Code.SUCCESS, "Success")

    def open_watch(self):
        return self.get({"action": "open"})
