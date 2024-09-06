from fastapi.testclient import TestClient
from pytest import fixture
from sqlalchemy.future.engine import Engine, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from myapp.executable.common import State
from myapp.executable.main import get_app_fastapi


@fixture()
def state() -> State:
    state = State()
    return state


@fixture()
def api_client(state: State) -> TestClient:
    app = get_app_fastapi(state)
    test_app = TestClient(app)
    return test_app
