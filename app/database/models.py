from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy import String
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from config import DB_URL

engine = create_async_engine(url=DB_URL, echo=True)

async_session = async_sessionmaker(engine)


Base = declarative_base()


class RequestHistory(Base):
    __tablename__ = 'request_history'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    request_time = Column(DateTime, default=datetime.utcnow)
    product_code = Column(String, nullable=False)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
