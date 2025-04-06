import asyncio

import httpx
from aiogram import Bot, Router, types
from aiogram.filters import Command, CommandStart

from src.config import get_settings
from src.keyboards.builders import main_markup

router = Router(name="common")
settings = get_settings()

HTTP_SUCCESS_CODE = 200
HEALTHY_RESPONSE_TEXT = "1"


@router.message(CommandStart())
async def start(message: types.Message) -> None:
    await message.answer(
        "Welcome! Click the button below to open the Mini App:", reply_markup=main_markup
    )


@router.message(Command("webhook_info"))
async def cmd_webhook_info(message: types.Message, bot: Bot):
    info = await bot.get_webhook_info()
    await message.answer(f"Webhook info:\n{info}")


@router.message(Command("healthcheck"))
async def check_health(message: types.Message):
    services = {
        "API": f"{settings.API.url}/api/v1/public/healthcheck",
        "MINI APP": f"{settings.MINIAPP.url}/api/healthcheck",
        "WEB": f"{settings.WEB.url}/api/healthcheck",
    }

    status_messages = [f"🔍 Checking {service}..." for service in services]
    progress_message = await message.answer("Service Healthcheck\n\n" + "\n".join(status_messages))

    async with httpx.AsyncClient() as client:
        tasks = {service: client.get(url, timeout=5.0) for service, url in services.items()}

        for service, task in tasks.items():
            try:
                response = await task
                is_ok = response.status_code == HTTP_SUCCESS_CODE
                emoji = "✅" if is_ok else "❌"
                status_messages = [
                    f"{emoji} {service}" if s == f"🔍 Checking {service}..." else s
                    for s in status_messages
                ]
                await progress_message.edit_text(
                    "Service Healthcheck\n\n" + "\n".join(status_messages)
                )
            except Exception:  # noqa: BLE001
                status_messages = [
                    f"❌ {service} is unavailable" if s == f"🔍 Checking {service}..." else s
                    for s in status_messages
                ]
                await progress_message.edit_text(
                    "Service Healthcheck\n\n" + "\n".join(status_messages)
                )
            await asyncio.sleep(0.3)

    all_ok = all(
        any(s.startswith("✅") for s in status_messages if service in s) for service in services
    )
    header = "✅ All services are operational" if all_ok else "⚠️ Service Status Report"
    await progress_message.edit_text(f"{header}\n\n" + "\n".join(status_messages))
