from pydantic import BaseModel
from sqlalchemy import Column, Integer, MetaData, String
from sqlalchemy.orm import declarative_base


class EventBucketAddReq(BaseModel):
    title: str
    message: str


class EventBucketAddResp(BaseModel):
    uuid: str


class FullEvent(BaseModel):
    event_bucket: str
    event_id: str
    title: str
    message: str


class EventList(BaseModel):
    events: list[str]


metadata = MetaData()
Base = declarative_base(metadata=metadata)


class EventsSql(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    event_bucket = Column(String(50), nullable=False)
    event_id = Column(String(50), nullable=False)
    title = Column(String(50), nullable=False)
    message = Column(String(50), nullable=False)

    __tablename__ = "events"
