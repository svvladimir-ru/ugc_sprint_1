
from logging import Logger
from uuid import UUID

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

from .tools import benchmark, parse_error


class MongoManager:

    search_keys = ['user_id', 'movie_id', 'content_id']

    def __init__(self, client: MongoClient, logger: Logger):
        self.client = client
        self.logger = logger

    def correct_data_for_search(self, data: dict) -> dict:
        new_data = data.copy()
        for key in data:
            if key not in self.search_keys:
                del new_data[key]

        return new_data

    def read_random(self, collection: str) -> [UUID, None]:
        try:
            random_data = self.client[collection].aggregate(
                [{"$sample": {"size": 1}}]
            )
            returned = random_data._CommandCursor__data[0]['_id']
            return returned
        except IndexError:
            return None

    @benchmark(operation='Одиночное добавление')
    def create(self, data: dict, collection: str) -> None:
        try:
            self.client[collection].insert_one(data)
        except DuplicateKeyError:
            query = self.correct_data_for_search(data)
            self.search(collection=collection, query_data=query)
        except Exception as e:
            self.logger.info(f"Ошибка при одиночной вставке: {e}")

    @benchmark(operation='Множественное добавление')
    def create_many(self, data: list[dict], collection: str) -> None:
        try:
            self.client[collection].insert_many(data)
        except Exception as e:
            queries = parse_error(e.args[0])
            for query in queries:
                self.search(collection=collection, query_data=query)

    @benchmark(operation='Поиск')
    def search(self, collection: str, query_data: dict) -> None:
        try:
            result = self.client[collection].count_documents(query_data)
            self.logger.info(f"Найденных объектов: {result}")
        except Exception as e:
            self.logger.info(f"Ошибка при поисковом запросе: {e}")
