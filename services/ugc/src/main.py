import logging

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from aiokafka import AIOKafkaProducer

from api.v1 import events
from core import config
from core.logger import LOGGING
from db import kafka


module_logger = logging.getLogger('Main')


def kafka_meta_update_listener(meta):
    module_logger.info('Kafka meta updated: %s', meta.topics())


app = FastAPI(
    title=config.PROJECT_NAME,
    description='API for posting user-generated content events to UGC db',
    docs_url='/ugc/openapi',
    openapi_url='/ugc/openapi.json',
    default_response_class=ORJSONResponse
)


@app.on_event('startup')
async def startup():
    kafka.kafka = AIOKafkaProducer(bootstrap_servers='{host}:{port}'.format(host=config.KAFKA_HOST,
                                                                            port=config.KAFKA_PORT),
                                   metadata_max_age_ms=config.KAFKA_CLIENT_METADATA_TTL * 1000)
    kafka.kafka.client.cluster.add_listener(kafka_meta_update_listener)
    await kafka.kafka.start()


@app.on_event('shutdown')
async def shutdown():
    await kafka.kafka.stop()


app.include_router(events.router, prefix='/ugc/v1/events', tags=['events'])


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8001, log_config=LOGGING, log_level=logging.DEBUG, debug=True)
