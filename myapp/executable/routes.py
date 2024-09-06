from uuid import UUID

import fastapi

from myapp.executable.common import EVENT_BUCKET_PATTERN, State_
from myapp.executable.models import (
    EventBucketAddReq,
    EventBucketAddResp,
    EventList,
    EventsSql,
    FullEvent,
)

router = fastapi.APIRouter(prefix="/v1")


@router.put(
    "/{event_bucket}",
    status_code=fastapi.status.HTTP_201_CREATED,
    response_model=EventBucketAddResp,
)
def event_bucket_put(
    state: State_,
    body: EventBucketAddReq,
    event_bucket: str = fastapi.Path(..., pattern=EVENT_BUCKET_PATTERN),
) -> EventBucketAddResp:
    uuid = state.get_uuid()
    data = EventsSql(
        event_bucket=event_bucket, event_id=uuid, title=body.title, message=body.message
    )
    state.logger.info("Writing to database")
    with state.sessionmaker() as session:
        session.add(data)
        session.commit()

    return EventBucketAddResp(uuid=uuid)


@router.get(
    "/{event_bucket}", status_code=fastapi.status.HTTP_200_OK, response_model=EventList
)
def event_bucket_get(
    state: State_,
    event_bucket: str = fastapi.Path(..., pattern=EVENT_BUCKET_PATTERN),
) -> str:
    state.logger.info("Querying database for event_bucket")
    with state.sessionmaker() as session:
        data = (
            session.query(EventsSql.event_id)
            .where(EventsSql.event_bucket == event_bucket)
            .all()
        )

    if len(data) == 0:
        state.logger.error(f"{event_bucket} not found")
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail=f"{event_bucket} does not exist.",
        )

    events = [event[0] for event in data]
    return EventList(events=events)


@router.get(
    "/{event_bucket}/{event_id}",
    status_code=fastapi.status.HTTP_200_OK,
    response_model=FullEvent,
)
def event_bucket_id_get(
    state: State_,
    event_bucket: str = fastapi.Path(..., pattern=EVENT_BUCKET_PATTERN),
    event_id: UUID = fastapi.Path(...),
) -> str:
    state.logger.info("Querying database for event_bucket and event_id")
    with state.sessionmaker() as session:
        data = (
            session.query(EventsSql)
            .where(EventsSql.event_bucket == event_bucket)
            .where(EventsSql.event_id == str(event_id))
            .one_or_none()
        )

    if data is None:
        state.logger.error(f"{event_id} for {event_bucket} not found")
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail=f"{event_id} in {event_bucket} does not exist.",
        )

    return FullEvent(
        event_bucket=data.event_bucket,
        event_id=data.event_id,
        title=data.title,
        message=data.message,
    )
