from typing import Optional
from uuid import UUID
import random

from models import Likes, Reviews, Bookmarks, BaseCollection
from config import ModulesConfigs
from .mongo import MongoManager


class Generator:

    current_user = None
    current_movie = None

    def __init__(self, mongo_manager: MongoManager, configs: ModulesConfigs):
        self.mongo_manager = mongo_manager
        self.users_count = configs.users_count
        self.movies_count = configs.movies_count
        self.text_list = configs.text_list

    def generate_start_data(self) -> BaseCollection:
        last_value = self.movies_count + self.users_count
        counter = 0
        for i in range(0, last_value):
            collection = 'users' if counter >= self.movies_count else 'movie'
            counter += 1
            yield BaseCollection(collection=collection)

    def get_base_data(self, reviews: Optional[bool] = False) -> [UUID, UUID]:
        user_id = self.mongo_manager.read_random(collection='users')

        if reviews:
            review_id = self.mongo_manager.read_random(collection='reviews')
            return user_id, review_id

        movie_id = self.mongo_manager.read_random(collection='movie')
        return user_id, movie_id

    def generate_like(self) -> [Likes, None]:
        event = not random.getrandbits(1)
        if event:
            user_id, content_id = self.get_base_data()
            value = random.randint(0, 10)
        else:
            user_id, content_id = self.get_base_data(reviews=True)
            value = random.randint(0, 1)

        if content_id is None:
            return None

        data = {
            "user_id": user_id,
            "content_id": content_id,
            "value": value
        }

        return Likes.parse_obj(data)

    def generate_review(self) -> [Reviews, None]:
        user_id, movie_id = self.get_base_data()
        text = self.text_list[random.randint(0, 2)]

        if user_id is None or movie_id is None:
            return None

        data = {
            "user_id": user_id,
            "movie_id": movie_id,
            "text": text
        }
        return Reviews.parse_obj(data)

    def generate_bookmarks(self) -> [Bookmarks, None]:
        user_id, movie_id = self.get_base_data()

        if user_id is None or movie_id is None:
            return None

        data = {
            "user_id": user_id,
            "movie_id": movie_id,
        }
        return Bookmarks.parse_obj(data)

    def generate_data(self):
        while True:
            event = random.randint(1, 3)
            if event == 1:
                data = self.generate_like()
            elif event == 2:
                data = self.generate_review()
            else:
                data = self.generate_bookmarks()

            if data is None:
                continue

            yield data
