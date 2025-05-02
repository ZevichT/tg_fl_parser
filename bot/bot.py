from aiogram import Dispatcher

from .router import router, bot


dp = Dispatcher()
dp.include_routers(router)


async def main():
    await dp.start_polling(bot)