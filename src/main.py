from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import setup_application
from aiohttp import web

from src.config import get_settings
from src.handlers import setup_routers

settings = get_settings()
bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()


async def on_startup(app: web.Application):
    bot = app["bot"]
    await bot.set_webhook(
        url=settings.WEBHOOK_URL,
        allowed_updates=dp.resolve_used_update_types(),
        drop_pending_updates=True,
    )


def create_app():
    setup_routers(dp)

    app = web.Application()
    app["bot"] = bot

    app.on_startup.append(on_startup)

    setup_application(app, dp, bot=bot)
    return app


if __name__ == "__main__":
    web.run_app(create_app(), port=8000)
