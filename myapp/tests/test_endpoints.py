from uuid import UUID

from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.future.engine import Engine

from myapp.executable.common import State
from myapp.executable.models import EventBucketAddReq, EventList, EventsSql, FullEvent


def test_health(api_client: TestClient) -> None:
    resp = api_client.get("/health")
    assert resp.status_code == status.HTTP_200_OK


def test_put_incorrect_data(api_client: TestClient) -> None:
    event_bucket = "123!"
    resp = api_client.put(f"/v1/{event_bucket}")
    assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    event_bucket = "123"
    resp = api_client.put(f"/v1/{event_bucket}")
    assert resp.status_code != status.HTTP_201_CREATED


def test_put_correct_data(api_client: TestClient, state: State) -> None:
    event_bucket = "123"
    req = EventBucketAddReq(title="This 123 event", message="Pytest")
    resp = api_client.put(f"/v1/{event_bucket}", content=req.model_dump_json())
    assert resp.status_code == status.HTTP_201_CREATED
    event_id = resp.json()["uuid"]

    with state.sessionmaker() as session:
        data = (
            session.query(EventsSql)
            .where(EventsSql.event_bucket == event_bucket)
            .one_or_none()
        )
    assert data is not None
    assert data.event_bucket == event_bucket
    assert UUID(data.event_id)
    assert data.event_id == event_id
    assert data.title == req.title
    assert data.message == req.message

    event_bucket = "123"
    req = EventBucketAddReq(title="This 123 event", message="Pytest")
    resp = api_client.put(f"/v1/{event_bucket}", content=req.model_dump_json())
    assert resp.status_code == status.HTTP_201_CREATED
    event_id_repeat = resp.json()["uuid"]
    assert event_id != event_id_repeat


def test_get_correct_data(api_client: TestClient) -> None:
    event_bucket = "123"
    req = EventBucketAddReq(title="This 123 event", message="Pytest")
    resp = api_client.put(f"/v1/{event_bucket}", content=req.model_dump_json())
    assert resp.status_code == status.HTTP_201_CREATED
    event_id = resp.json()["uuid"]

    resp = api_client.get(f"/v1/{event_bucket}")
    assert resp.status_code == status.HTTP_200_OK
    events_list = EventList.model_validate(resp.json())

    assert len(events_list.events) == 1
    assert events_list.events[0] == event_id

    resp = api_client.get(f"/v1/{event_bucket}/{event_id}")
    assert resp.status_code == status.HTTP_200_OK
    event = FullEvent.model_validate(resp.json())
    assert event.event_bucket == event_bucket
    assert event.event_id == event_id
    assert event.title == req.title
    assert event.message == req.message


def test_get_incorrect_data(api_client: TestClient, state: State) -> None:
    event_bucket = "123!"
    resp = api_client.get(f"/v1/{event_bucket}")
    assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    event_bucket = "123"
    req = EventBucketAddReq(title="This 123 event", message="Pytest")
    resp = api_client.put(f"/v1/{event_bucket}", content=req.model_dump_json())
    assert resp.status_code == status.HTTP_201_CREATED

    wrong_event_id = state.get_uuid()
    resp = api_client.get(f"/v1/{event_bucket}/{wrong_event_id}")
    assert resp.status_code == status.HTTP_404_NOT_FOUND

    wrong_event_bucket = "1234"
    resp = api_client.get(f"/v1/{wrong_event_bucket}")
    assert resp.status_code == status.HTTP_404_NOT_FOUND
    resp = api_client.get(f"/v1/{wrong_event_bucket}/{wrong_event_id}")
    assert resp.status_code == status.HTTP_404_NOT_FOUND


def test_wrong_verbs(api_client: TestClient, state: State) -> None:
    event_bucket = "123"
    resp = api_client.post(f"/v1/{event_bucket}")
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    event_id = state.get_uuid()
    resp = api_client.put(f"/v1/{event_bucket}/{event_id}")
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
