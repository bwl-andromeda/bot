import asyncio
import logging
from aiogram import (
    Bot, Dispatcher
)
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from bot.handlers import setup_routers
from config import (
    settings
)
from database.models.engine import (
    create_db, close_connection, drob_db
)


async def on_startup() -> None:
    await create_db()


async def on_shutdown() -> None:
    await close_connection()


async def main() -> None:
    bot = Bot(
        settings.TOKEN.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.include_router(setup_routers())
    await bot.delete_webhook(True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
