import asyncio
import logging

from bot.loader import bot, dp
from handlers import errors, start, ayah, review, quiz, stats
from scheduler import setup_scheduler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)


async def main():
    dp.include_router(errors.router)
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
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
