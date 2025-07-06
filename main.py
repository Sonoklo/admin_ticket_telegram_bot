import asyncio
from config import BOT_TOKEN
from aiogram import Dispatcher,Bot
from handlers import fsm,text

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

dp.include_routers(fsm.router,text.router)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    

