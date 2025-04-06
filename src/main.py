import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from src.config import get_settings
from src.handlers import setup_routers

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

settings = get_settings()

bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))

dp = Dispatcher()


async def log_errors_middleware(handler, event, data):
    try:
        logger.debug("Incoming update: %s", event)
        return await handler(event, data)
    except Exception:
        logger.exception("Error processing update")
        raise


dp.update.middleware(log_errors_middleware)


async def on_startup(app: web.Application):
    try:
        webhook_url = f"{settings.WEBHOOK_URL}/webhook"
        logger.info("Setting webhook to %s", webhook_url)
        await bot.set_webhook(
            url=webhook_url,
            allowed_updates=dp.resolve_used_update_types(),
            drop_pending_updates=True,
            secret_token=settings.BOT_SECRET,
        )
    except Exception:
        logger.exception("Webhook setup failed")
        raise


async def on_shutdown(app: web.Application):
    await bot.delete_webhook()
    await bot.session.close()
    logger.info("Bot stopped")


def create_app() -> web.Application:
    setup_routers(dp)

    app = web.Application()
    app["bot"] = bot

    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    webhook_route = "/webhook"
    SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=settings.BOT_SECRET,
    ).register(app, path=webhook_route)

    setup_application(app, dp, bot=bot)

    return app


if __name__ == "__main__":
    web.run_app(
        create_app(),
        port=settings.BOT_PORT,
        host=settings.BOT_HOST,
        access_log=logging.getLogger("aiohttp.access"),
    )
