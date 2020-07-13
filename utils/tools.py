import hashlib
import logging

logger = logging.getLogger(__name__)


def encrypt(strs):
    return hashlib.md5(strs.encode(encoding='UTF-8')).hexdigest()
