import threading
import uuid

REQUEST_ID_HEADER = 'HTTP_REQUEST_ID'
NO_REQUEST_ID = "none"  # Used if no request ID is available


class LocalVars:

    def __init__(self):
        self._local = threading.local()

    @staticmethod
    def _generate_id():
        return uuid.uuid4().hex

    @property
    def request_id(self):
        request_id = getattr(self._local, 'request_id', NO_REQUEST_ID)
        if request_id == NO_REQUEST_ID:
            request_id = self._generate_id()
            self._local.request_id = request_id
        return self._local.request_id

    @request_id.setter
    def request_id(self, value):
        if not value:
            value = self._generate_id()
        self._local.request_id = value

    @property
    def request_token(self):
        return getattr(self._local, 'request_token', '')

    @request_token.setter
    def request_token(self, value):
        self._local.request_token = value


local = LocalVars()
