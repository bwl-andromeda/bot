from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.models.all_models import User


async def add_user(session: AsyncSession, data: dict):
    obj = User(
        tg_id=data['tg_id'],
        tg_username=data['tg_username'],
        fio=data['fio'],
        phone=data['phone'],
        role=data['role']
    )
    session.add(obj)
    await session.commit()


async def get_user(session: AsyncSession, user_id: int):
    query = select(User).where(User.tg_id == user_id)
    result = await session.execute(query)
    return result.scalar_one_or_none()
