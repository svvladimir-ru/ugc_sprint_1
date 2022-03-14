from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class BaseCollection(BaseModel):
    id: Optional[UUID] = Field(alias='_id', default=uuid4())
    created_at: Optional[datetime] = datetime.now()
    collection: Optional[str]

    def __init__(self, collection: str = None, **kwargs):
        super().__init__(**kwargs)
        self.id = uuid4()
        self.created_at = datetime.now()
        if collection:
            self.collection = collection


class Likes(BaseCollection):
    user_id: UUID
    content_id: UUID
    value: int
    collection = "likes"


class Reviews(BaseCollection):
    user_id: UUID
    movie_id: UUID
    text: str
    collection = "reviews"


class Bookmarks(BaseCollection):
    movie_id: UUID
    user_id: UUID
    collection = "bookmarks"
