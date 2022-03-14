from fastapi import APIRouter, Depends

from auth_utils.required import AuthRequired, AuthInfo
from models.event import UGCEvent, UGCEventPosted
from services.events import EventsService, get_events_service


router = APIRouter()


@router.post('/',
             response_model=UGCEventPosted,
             description='Posting UGC events',
             response_description='Posted UGC event with timestamp')
async def post_event(event: UGCEvent,
                     auth_info: AuthInfo = Depends(AuthRequired(token_optional=False, validate_locally=True)),
                     service: EventsService = Depends(get_events_service)) -> UGCEventPosted:
    posted_event = await service.post_event(event)
    return posted_event
