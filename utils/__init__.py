
class Code:
    """
    错误码
    """
    SUCCESS = 'Success'
    UNKNOWN_ERROR = 'UnknownError'          # 未知错误
    RES_ERROR = 'ResopError'                # 请求resop失败
    UCENTER_ERROR = 'UcenterError'          # 请求ucenter失败
    PAAS_ERROR = 'PaasError'                # 请求Paas失败
    BILL_ERROR = 'BillError'                # 请求ucenter失败

    CONFIG_ERROR = 'ConfigError'            # 配置错误
    REQUEST_ERROR = 'RequestError'          # 请求错误
    PARAM_ERROR = 'ParameterInvalid'        # 参数错误
    DATA_EXISTS = 'DataExists'              # 数据已存在
    DATA_NOT_EXISTS = 'DataNotExists'       # 数据不存在
    DATA_DUPLICATION = 'DataDuplication'    # 数据重复
    TIMEOUT_ERROR = 'TimeOut'               # 请求超时


class CommonException(Exception):
    """
    工作流平台异常
    """
    def __init__(self, code, msg):
        self.code = code
        self.msg = msg
        super(CommonException, self).__init__('%s: %s' % (code, msg))


class CommonReturn:
    """
    工作流返回
    """
    def __init__(self, code='', msg='', data=None, response=None):
        self.code = code
        self.msg = msg
        self.data = data or {}
        self.response = response

    def is_success(self):
        if self.code in (Code.SUCCESS, '0000'):
            return True
        return False

    def to_json(self):
        return {
            'code': self.code,
            'msg': self.msg,
            'data': self.data
        }
