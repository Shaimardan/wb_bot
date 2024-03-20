from app.database.models import RequestHistory
from app.database.models import async_session


async def add_subscribe_id(user_id, product_code):
    async with async_session() as session:
        session.add(RequestHistory(user_id=user_id, product_code=product_code))
        await session.commit()
