import logging

from models import Model

logger = logging.getLogger(__name__)


class User(Model):

    def __init__(self, name, email, password, create_time=None, update_time=None):
        self.name = name
        self.email = email
        self.password = password
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
            'password': self.password
        }
