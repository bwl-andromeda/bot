from sqlalchemy import BigInteger, VARCHAR, DateTime, func
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


class Base(AsyncAttrs, DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now())


class User(Base):
    __tablename__ = "user"

    tg_id = mapped_column(BigInteger, primary_key=True)
    tg_username = mapped_column(VARCHAR(50), nullable=True)
    fio: Mapped[str] = mapped_column(nullable=True)
    phone: Mapped[str] = mapped_column(nullable=True)
    role = mapped_column(VARCHAR(50), nullable=True)
