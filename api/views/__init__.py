import logging
from functools import wraps

from django.http import HttpResponse
from rest_framework.response import Response

from utils import CommonException, Code

logger = logging.getLogger(__name__)


def api_decorator(api_name, serializer_class=None):
    """
    统一处理api接口序列化参数验证
    """
    def _wrapper(func):

        @wraps(func)
        def deco(*args, **kwargs):
            try:
                self = args[0]      # ViewSet instance from args[0]
                req = args[1]       # request instance from args[1]
                req_data = {
                    'GET': req.GET.dict(),
                    'POST': req.data,
                    'PUT': req.data,
                    'DELETE': req.data
                }.get(req.method)
                # 获取ViewSet自定义序列化类
                obj_serializer_class = serializer_class
                if not obj_serializer_class:
                    obj_serializer_class = self.serializer_class
                serializer_data = None
                if obj_serializer_class:
                    # 序列化数据验证
                    serializer_data = obj_serializer_class(data=req_data)
                    if not serializer_data.is_valid():
                        res = {
                            'code': Code.PARAM_ERROR,
                            'msg': serializer_data.errors
                        }
                        return Response(res, status=400)
                if serializer_data:
                    kwargs['params'] = serializer_data.data
                # 返回CommonReturn对象
                res = func(*args, **kwargs)
                status = None
                if not res.is_success():
                    status = 500
                if res.response:
                    # 返回对象有自定义Response实例
                    res = res.response
                else:
                    res = res.to_json()
            except CommonException as exc:
                logger.error('%s error: %s' % (api_name, exc), exc_info=True)
                res = {'code': exc.code, 'msg': exc.msg}
                status = 500
            except Exception as exc:
                msg = '%s error: %s' % (api_name, exc)
                logger.error(msg, exc_info=True)
                res = {'code': Code.UNKNOWN_ERROR, 'msg': msg}
                status = 500
            logger.info('res: %s' % res)
            return Response(res, status=status)
        return deco

    return _wrapper


def health(req):
    return HttpResponse('ok')
