import logging

from models import Model

logger = logging.getLogger(__name__)


class Token(Model):

    def __init__(self, token='', username='', create_time=None, update_time=None):
        self.token = token
        self.username = username
        self.create_time = create_time
        self.update_time = update_time
        super().__init__()

    @property
    def primary_key(self):
        return self.token

    def repr(self):
        return {
            'token': self.token,
            'username': self.username
        }
