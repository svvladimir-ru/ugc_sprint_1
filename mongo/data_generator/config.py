import os
import logging

from pydantic import BaseSettings


# Настройка и инициализация логирования
def set_logger() -> logging.Logger:
    logger = logging.getLogger(__name__)
    logger.setLevel('DEBUG')
    handler = logging.StreamHandler()
    log_format = '%(asctime)s | %(levelname)s --> %(message)s'
    formatter = logging.Formatter(log_format)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


class ModulesConfigs(BaseSettings):
    text_list = [
        'Фильм хороший',
        'Фильм плохой',
        'Фильм на раз. Повторно смотреть бы не стал.'
    ]
    users_count = int(os.environ.get('USERS_COUNT', 10))
    movies_count = int(os.environ.get('MOVIES_COUNT', 10))


class GeneratorConfigs(BaseSettings):
    db_name = os.environ.get('MONGODB_NAME', 'movies')
    host = os.environ.get('MONGODB_HOST', 'localhost')
    port = os.environ.get('MONGO_PORT', 27017)
    login = os.environ.get('MONGODB_USERNAME', 'MongoUser')
    password = os.environ.get('MONGODB_PASSWORD', 'MongoPassword')
    connection_str = "mongodb://{login}:{password}@{host}:{port}"
    max_batch_size = int(os.environ.get('MAX_BATCH_SIZE', 10))
    modules_configs = ModulesConfigs()
    logger = set_logger()
