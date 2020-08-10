import logging

from service.kuberesource import KubeResource

logger = logging.getLogger(__name__)


class PodResource(KubeResource):

    RESOURCE_TYPE = 'pod'

    EXEC_ACTION = 'exec'
    STDIN_ACTION = 'stdin'
    OPENLOG_ACTION = 'openLog'
    CLOSELOG_ACTION = 'closeLog'

    def exec(self, params=None):
        res = self.request(self.EXEC_ACTION, params=params)
        return res

    def stdin(self, params=None):
        res = self.request(self.STDIN_ACTION, params=params)
        return res

    def open_log(self, params=None):
        res = self.request(self.OPENLOG_ACTION, params=params)
        return res

    def close_log(self, params=None):
        res = self.request(self.CLOSELOG_ACTION, params=params)
        return res
