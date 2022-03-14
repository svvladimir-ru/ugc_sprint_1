import os
from logging import config as logging_config

from core.logger import LOGGING


logging_config.dictConfig(LOGGING)

PROJECT_NAME = 'UGC Events post API v1'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

KAFKA_HOST = os.getenv('UGC_KAFKA_HOST', '127.0.0.1')
KAFKA_PORT = int(os.getenv('UGC_KAFKA_PORT', 9092))
KAFKA_CLIENT_METADATA_TTL = 30

DEFAULT_TOPIC = os.getenv('UGC_DEFAULT_TOPIC', 'misc')
