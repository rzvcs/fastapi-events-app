from fastapi.testclient import TestClient
from pytest import fixture
from sqlalchemy.future.engine import Engine, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from myapp.executable.common import State
from myapp.executable.main import get_app_fastapi


@fixture()
def sql_engine() -> Engine:
    # https://stackoverflow.com/questions/21766960/operationalerror-no-such-table-in-flask-with-sqlalchemy
    return create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )


@fixture()
def state(sql_engine: Engine) -> State:
    state = State()
    state.engine = sql_engine
    state.sessionmaker = sessionmaker(state.engine)
    return state


@fixture()
def api_client(state: State) -> TestClient:
    app = get_app_fastapi(state)
    test_app = TestClient(app)
    return test_app
