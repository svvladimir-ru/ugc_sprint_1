import logging
from datetime import datetime
from functools import lru_cache

from aiokafka import AIOKafkaProducer
from fastapi import Depends

from core import config
from db.kafka import get_kafka
from models.event import UGCEvent, UGCEventPosted


module_logger = logging.getLogger('EventsService')


_event_keys: dict[str, tuple[str, ...]] = {
    'movies_user_watched_sec': ('user_id', 'movie_id')
}


class EventsService:
    def __init__(self, kafka: AIOKafkaProducer):
        self.kafka = kafka

    async def post_event(self, event: UGCEvent) -> UGCEventPosted:
        topic = self._get_topic(event.type)
        key = self._get_key(event)

        module_logger.debug('Posting event {%s} to topic "%s" with key "%s"', event, topic, key)

        posted_event = UGCEventPosted(**event.dict(), posted_at=datetime.utcnow())
        await self.kafka.send_and_wait(topic=topic,
                                       key=key.encode(),
                                       value=posted_event.json().encode())
        return posted_event

    @staticmethod
    def _get_key(event: UGCEvent) -> str:
        ids = {'user_id': str(event.user_id),
               'movie_id': (event.data or {}).get('movie_id')}

        key_fields = _event_keys.get(event.type)
        if key_fields:
            key = '+'.join(ids[field] for field in key_fields)  # type: ignore[misc]
        else:
            key = ids['movie_id'] or ids['user_id']  # type: ignore[assignment]

        return key

    def _get_topic(self, event_type: str) -> str:
        topic = event_type.split('_', maxsplit=1)[0]
        if topic not in self.kafka.client.cluster.topics():
            module_logger.info("Event topic doesn't exist in kafka, choosing default topic '%s'", config.DEFAULT_TOPIC)
            topic = config.DEFAULT_TOPIC
        return topic


@lru_cache()
def get_events_service(kafka: AIOKafkaProducer = Depends(get_kafka)) -> EventsService:
    return EventsService(kafka)
