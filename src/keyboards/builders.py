from aiogram.types import WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.config import get_settings

settings = get_settings()
main_markup = (
    InlineKeyboardBuilder().button(
        text="Open Mini App", web_app=WebAppInfo(url=settings.WEBAPP_URL)
    )
).as_markup()
