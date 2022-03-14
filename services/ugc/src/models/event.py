from datetime import datetime
from typing import Optional
from uuid import UUID

import orjson
from pydantic import BaseModel, Field


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class BaseUGCModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class UGCEvent(BaseUGCModel):
    type: str = Field(..., description='Type of event', example='movies_user_watched_sec')
    user_id: UUID = Field(..., description='Id of a user who generated the event')
    data: Optional[dict] = Field(None, description='Additional event data', example={
                                     'movie_id': 'fb4df957-f3f0-4508-8062-c561d96b3d9a',
                                     'movie_sec': 3600
                                 })


class UGCEventPosted(UGCEvent):
    posted_at: Optional[datetime] = Field(None, description='When the event was posted')
