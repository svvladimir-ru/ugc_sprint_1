import json

import backoff
from clickhouse_driver import Client
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable
from kafka.structs import OffsetAndMetadata
from kafka import TopicPartition

from conf import settings


def create_tables(client) -> None:
    client.execute(
        """CREATE TABLE IF NOT EXISTS views (
            id String,
            user_id String,
            ip String,
            movie_id String,
            timestamp_movie Int64,
            time Int64
            ) Engine=MergeTree() ORDER BY id
     """)


@backoff.on_exception(backoff.expo, Exception, max_tries=3)
def insert_clickhouse(client, data: list) -> None:
    client.execute(
        '''
        INSERT INTO views (
        id, user_id, ip, movie_id, timestamp_movie, time)  VALUES {}
        '''.format(", ".join("("+i+")" for i in data)))


def etl_process(consumer: KafkaConsumer, clickhouse_client: Client) -> None:
    data = []
    for msg in consumer:
        data.append((', '.join(json.loads(msg.value.decode('utf-8')).values())))
        if len(data) == 100:
            insert_clickhouse(clickhouse_client, data)
            data.clear()
            tp = TopicPartition(settings.KAFKA_TOPICS, msg.partition)
            options = {tp: OffsetAndMetadata(msg.offset + 1, None)}
            consumer.commit(options)


@backoff.on_exception(backoff.expo, NoBrokersAvailable)
def main() -> None:
    consumer = KafkaConsumer(
        settings.KAFKA_TOPICS,
        bootstrap_servers=[f'{settings.KAFKA_HOST}:{settings.KAFKA_PORT}'],
        group_id=settings.kafka_group,
        auto_offset_reset='earliest',
        enable_auto_commit=False
    )
    clickhouse_client = Client(host=settings.CLICKHOUSE_HOST, port=settings.CLICKHOUSE_POST)

    create_tables(clickhouse_client)
    etl_process(consumer, clickhouse_client)


if __name__ == '__main__':
    main()
