import httpx
from aiogram import Router, types
from aiogram.filters import Command, CommandStart

from src.config import get_settings

router = Router(name="common")
settings = get_settings()


@router.message(CommandStart())
async def start(message: types.Message) -> None:
    await message.answer("Open Mini App")


@router.message(Command("healthcheck"))
async def check_health(message: types.Message):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://localhost:8001/api/v1/public/healthcheck",
                timeout=5.0,
            )
            if response.status_code == 200 and response.text == "1":  # noqa: PLR2004
                await message.answer("✅ API is healthy!")
            else:
                await message.answer(
                    f"⚠️ Unexpected response: {response.status_code} | {response.text}"
                )
    except Exception as e:  # noqa: BLE001
        await message.answer(f"❌ Connection failed: {e!s}")
