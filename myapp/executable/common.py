import logging
from logging.handlers import RotatingFileHandler
from typing import Annotated
from uuid import uuid4

import fastapi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from myapp.executable.models import Base, EventsSql


class State:
    def __init__(self) -> None:
        self.logger = logging.getLogger("executable")
        handler = RotatingFileHandler("/tmp/app.log", maxBytes=2000, backupCount=10)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

        # https://stackoverflow.com/questions/21766960/operationalerror-no-such-table-in-flask-with-sqlalchemy
        self.logger.info("create in memory engine")
        self.engine = create_engine(
            "sqlite:///:memory:",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        self.sessionmaker = sessionmaker(self.engine)

    def create_events_table(self) -> None:
        Base.metadata.create_all(self.engine)

    def get_uuid(self) -> str:
        """
        In lack of a REDIS source to keep a universal UUID, generate a unique one in 10
        retries.
        """
        try_attempt = 1
        retries = 10
        while try_attempt != retries:
            self.logger.info(f"Getting UUID; try: {try_attempt}")
            uuid = str(uuid4())
            with self.sessionmaker() as session:
                event_id = (
                    session.query(EventsSql.event_id)
                    .where(EventsSql.event_id == uuid)
                    .one_or_none()
                )
            if event_id is None:
                self.logger.info(f"Got uuid on try {try_attempt}")
                return uuid
            try_attempt = try_attempt + 1

        raise RuntimeError(f"Could not get uuid in {retries} retires")


def fastapi_get_state_(request: fastapi.Request) -> State:
    state: State = request.app.state.mystate
    return state


State_ = Annotated[State, fastapi.Depends(fastapi_get_state_)]

EVENT_BUCKET_PATTERN = r"^[a-zA-Z0-9-_]+$"
