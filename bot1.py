import asyncio
import logging

from bot.loader import bot, dp
from bot.handlers import start, ayah, review, quiz, stats
from scheduler import setup_scheduler

logging.basicConfig(level=logging.INFO)


async def main():
    dp.include_router(start.router)
    dp.include_router(ayah.router)
    dp.include_router(review.router)
    dp.include_router(quiz.router)
    dp.include_router(stats.router)

    scheduler = setup_scheduler(bot)
    scheduler.start()
    logging.info("Scheduler started.")

    try:
        await dp.start_polling(bot)
    finally:
        scheduler.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
