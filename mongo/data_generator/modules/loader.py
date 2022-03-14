from logging import Logger
from random import randint

from .generator import Generator
from .mongo import MongoManager
from models import BaseCollection


class Loader:

    batch_size = 1
    batch = {}

    def __init__(self, mongo_manager: MongoManager,
                 generator: Generator,
                 max_batch_size: int, logger: Logger):
        self.generator = generator
        self.logger = logger
        self.mongo_manager = mongo_manager

        self.min_batch_size = 1
        self.max_batch_size = max_batch_size
        self.change_batch_size()

    def change_batch_size(self):
        self.batch_size = randint(self.min_batch_size, self.max_batch_size)

    def load(self, data: BaseCollection):
        collection = data.collection
        dict_data = data.dict(by_alias=True, exclude={'collection'})
        if self.batch_size == 1:
            self.mongo_manager.create(
                data=dict_data,
                collection=collection
            )
            self.change_batch_size()
            return
        try:
            if len(self.batch[data.collection]) == self.batch_size:
                self.logger.info(
                    f"Размер объекта для добавления: {self.batch_size}"
                )
                self.mongo_manager.create_many(
                    data=self.batch[collection],
                    collection=collection
                )
                self.change_batch_size()
                self.batch[data.collection] = []
        except KeyError:
            self.batch[data.collection] = []

        self.batch[data.collection].append(dict_data)

    def load_start_data(self):
        for data in self.generator.generate_start_data():
            self.load(data=data)

        for collection in self.batch:
            if len(self.batch[collection]) != 0:
                self.mongo_manager.create_many(
                    data=self.batch[collection],
                    collection=collection
                )

        self.change_batch_size()

    def run(self):
        self.load_start_data()
        for data in self.generator.generate_data():
            self.load(data=data)
