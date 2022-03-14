from pydantic import BaseSettings, PyObject
from typing import Any


class Settings(BaseSettings):
    KAFKA_HOST: str = '0.0.0.0'
    KAFKA_PORT: int = 9092
    kafka_group: str = 'from-kafka-to-clickhouse-etl'
    CLICKHOUSE_HOST: str = '0.0.0.0'
    CLICKHOUSE_POST: int = 9000
    KAFKA_TOPICS: str = 'movies'

    class Config:
        env_file = '.env.dev'
        env_prefix = 'UGC_'


settings = Settings()
