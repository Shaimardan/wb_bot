import asyncio

from aiogram import Dispatcher
from app.database.models import async_main
from app.handlers import router
from app.admin import admin
from main import bot


async def main():
    await async_main()
    dp = Dispatcher()
    dp.include_routers(admin, router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')