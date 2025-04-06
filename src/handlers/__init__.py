from . import common


def setup_routers(dp) -> None:
    dp.include_router(common.router)
