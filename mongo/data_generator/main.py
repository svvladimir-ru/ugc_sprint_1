from pymongo import MongoClient

from config import GeneratorConfigs
from modules import Loader, Generator, MongoManager


if __name__ == '__main__':
    configs = GeneratorConfigs()
    connection_str = configs.connection_str.format(
        login=configs.login,
        password=configs.password,
        host=configs.host,
        port=configs.port
    )
    client = MongoClient(
        connection_str,
        serverSelectionTimeoutMS=5000,
        uuidRepresentation='standard'
    )
    db = client[configs.db_name]
    mongo = MongoManager(client=db, logger=configs.logger)
    generator = Generator(mongo_manager=mongo, configs=configs.modules_configs)
    loader = Loader(
        mongo_manager=mongo,
        generator=generator,
        logger=configs.logger,
        max_batch_size=configs.max_batch_size
    )
    loader.run()
