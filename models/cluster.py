import logging
import uuid

from models import Model

logger = logging.getLogger(__name__)


class Cluster(Model):

    def __init__(self, name=None, token=None, create_time=None, update_time=None):
        self.name = name
        self.token = token
        self.create_time = create_time
        self.update_time = update_time
        super().__init__()

    @property
    def primary_key(self):
        return self.name

    def repr(self):
        return {
            'name': self.name,
            'token': self.token
        }

    @classmethod
    def gen_token(cls):
        return str(uuid.uuid4().hex)

    def save(self):
        if not self.token:
            self.token = self.gen_token()
        return super().save()
