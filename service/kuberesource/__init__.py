import json
import logging

from service.middlemessage import MiddleMessage, MiddleRequest
from utils import CommonException, CommonReturn, Code

logger = logging.getLogger(__name__)


class KubeResource:

    RESOURCE_TYPE = None

    LIST_ACTION = 'list'

    def __init__(self, cluster=None):
        self.cluster = cluster
        self.middle_message = MiddleMessage()

    def list(self, params=None):
        res = self.request(self.LIST_ACTION, params=params)
        return res

    def request(self, action, params=None, timeout=30):
        try:
            middle_request = MiddleRequest(cluster=self.cluster,
                                           resource=self.RESOURCE_TYPE,
                                           action=action,
                                           params=params,
                                           timeout=timeout)
            res_data = self.middle_message.send_request(middle_request)
            json_data = json.loads(res_data)
            return CommonReturn(code=json_data.get('code'),
                                msg=json_data.get('msg'),
                                data=json_data.get('data'))
        except CommonException as exc:
            logger.error('request error: %s' % exc, exc_info=True)
            return CommonReturn(exc.code, exc.msg)
        except Exception as exc:
            logger.error('request error: %s' % exc, exc_info=True)
            return CommonReturn(Code.UNKNOWN_ERROR, 'request error：%s' % exc)
