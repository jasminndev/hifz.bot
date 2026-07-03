import logging

from aiogram import Router
from aiogram.types import ErrorEvent

logger = logging.getLogger(__name__)
router = Router()


@router.error()
async def global_error_handler(event: ErrorEvent):
    logger.exception(
        f"Kutilmagan xato: {event.exception}",
        exc_info=event.exception,
    )

    update = event.update
    try:
        if update.message:
            await update.message.answer(
                "😔 Kechirasiz, xatolik yuz berdi.\n"
                "Iltimos, qaytadan urinib ko'ring yoki /start bosing."
            )
        elif update.callback_query:
            await update.callback_query.answer(
                "Xatolik yuz berdi, qaytadan urinib ko'ring.",
                show_alert=True,
            )
    except Exception:
        pass

    return True
