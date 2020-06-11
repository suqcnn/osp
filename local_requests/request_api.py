import json
import logging
import requests

from local_requests import local
from utils import CommonReturn, Code

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

logger = logging.getLogger(__name__)


class RequestAPI(object):

    @classmethod
    def access_data(cls, url, method, body=None, token='', timeout=None, access_headers=None, log_body=True):
        if url == '':
            return {'status': '2001', 'msg': 'path is empty!'}
        if method.upper() not in ('GET', 'POST', 'DELETE', 'PUT'):
            return {'status': '2002', 'msg': 'method is invalid!'}

        request_id = local.request_id

        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json; charset=UTF-8',
            'Request-Id': request_id
        }
        if token:
            headers['Access-Token'] = token
        if access_headers:
            headers.update(access_headers)

        target = urlparse(url)
        target_url = str(target.geturl())
        logger.info('request url: %s' % (target_url,))

        body = '' if method in ['GET'] else body
        if log_body:
            logger.info('request params: %s', json.dumps(body))

        method = method.lower()

        request_action = getattr(requests, method)

        try:
            r = request_action(target_url,
                               data=json.dumps(body),
                               headers=headers,
                               timeout=timeout)
            rtn_status = r.status_code
            logger.info('status %s, request result: %s' % (rtn_status, r.text))
            try:
                data = r.json()
                if 'code' in data:
                    return CommonReturn(data.get('code'),
                                        data.get('msg', '') or data.get('message', ''),
                                        data.get('data'))
                else:
                    return CommonReturn(Code.SUCCESS, data=data)
            except Exception as exc:
                logger.error('get return json error: %s' % exc, exc_info=True)
                msg = 'status code: %s, content: %s' % (rtn_status, r.content)
                return CommonReturn(Code.REQUEST_ERROR, msg)
        except requests.exceptions.ReadTimeout as exc:
            logger.error('response timeout: %s' % exc)
            return CommonReturn(Code.TIMEOUT_ERROR, 'Response timeout: %s' % (exc,))
        except requests.exceptions.Timeout as exc:
            logger.error('connect timeout: %s' % exc)
            return CommonReturn(Code.REQUEST_ERROR, 'Connect timeout: %s' % (exc,))
        except Exception as exc:
            logger.error('request error: %s' % exc, exc_info=True)
            return CommonReturn(Code.REQUEST_ERROR, 'request error: %s' % (exc,))

    @classmethod
    def access_data_v2(cls, url, method, params, token='', timeout=None, access_headers=None):
        """支持GET请求参数"""
        if url == '':
            return {'status': '2001', 'msg': 'path is empty!'}
        if method.upper() not in ('GET', 'POST', 'DELETE', 'PUT'):
            return {'status': '2002', 'msg': 'method is invalid!'}

        request_id = local.request_id

        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json; charset=UTF-8',
            'Request-Id': request_id
        }
        if token:
            headers['Access-Token'] = token
        if access_headers:
            headers.update(access_headers)

        target = urlparse(url)
        target_url = str(target.geturl())
        logger.info('request url: %s' % (target_url,))
        try:
            """
            r = request_action(target_url,
                               data=params,
                               headers=headers,
                               timeout=timeout)
            """
            r = requests.request(method, target_url, params=params, headers=headers, timeout=timeout)
            rtn_status = r.status_code
            logger.info('status %s, request result: %s' % (rtn_status, r.text))
            try:
                data = r.json()
                if 'code' in data:
                    return CommonReturn(data.get('code'),
                                        data.get('msg', '') or data.get('message', ''),
                                        data.get('data'))
                else:
                    return CommonReturn(Code.SUCCESS, data=data)
            except Exception as exc:
                logger.error('get return json error: %s' % exc, exc_info=True)
                msg = 'status code: %s, content: %s' % (rtn_status, r.content)
                return CommonReturn(Code.REQUEST_ERROR, msg)
        except requests.exceptions.ReadTimeout as exc:
            logger.error('response timeout: %s' % exc)
            return CommonReturn(Code.TIMEOUT_ERROR, 'Response timeout: %s' % (exc,))
        except requests.exceptions.Timeout as exc:
            logger.error('connect timeout: %s' % exc)
            return CommonReturn(Code.REQUEST_ERROR, 'Connect timeout: %s' % (exc,))
        except Exception as exc:
            logger.error('request error: %s' % exc, exc_info=True)
            return CommonReturn(Code.REQUEST_ERROR, 'request error: %s' % (exc,))
