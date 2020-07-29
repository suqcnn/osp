import logging

from models import Model

logger = logging.getLogger(__name__)


class User(Model):

    def __init__(self, name='', email='', password='', status='normal', last_login='', create_time=None, update_time=None):
        self.name = name
        self.email = email
        self.password = password
        self.status = status
        self.last_login = last_login
        self.create_time = create_time
        self.update_time = update_time

        super().__init__()

    @property
    def primary_key(self):
        return self.name

    def repr(self):
        return {
            'name': self.name,
            'email': self.email,
            'password': self.password,
            'status': self.status,
            'last_login': self.last_login
        }
