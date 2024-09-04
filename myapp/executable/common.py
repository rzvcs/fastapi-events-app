import logging
from typing import Annotated
from uuid import uuid4

import fastapi
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from myapp.executable.models import Base, EventsSql


class State:
    def __init__(self) -> None:
        self.logger = logging.getLogger("executable")
        self.engine = create_engine("sqlite:///main.db")
        self.sessionmaker = sessionmaker(self.engine)
        self.create_events_table()

    def create_events_table(self) -> None:
        Base.metadata.create_all(self.engine)

    def get_uuid(self) -> str:
        """
        In lack of a REDIS source to keep a universal UUID, generate a unique one in 10
        retries.
        """
        retries = 10
        while retries != 0:
            uuid = str(uuid4())
            # stmt = sqlalchemy.select(EventsSql.event_bucket).where(
            #     EventsSql.event_bucket == uuid
            # )
            # with self.engine.begin() as con:
            #     df = pd.read_sql_query(stmt, con=con)
            # if df["event_bucket"].size == 0:
            #     return uuid
            with self.sessionmaker() as session:
                event_bucket = (
                    session.query(EventsSql.event_bucket)
                    .where(EventsSql.event_bucket == uuid)
                    .one_or_none()
                )
            if event_bucket is None:
                return uuid
            retries = retries - 1


def fastapi_get_state_(request: fastapi.Request) -> State:
    state: State = request.app.state.mystate
    return state


State_ = Annotated[State, fastapi.Depends(fastapi_get_state_)]

EVENT_BUCKET_PATTERN = r"^[a-zA-Z0-9-_]+$"
