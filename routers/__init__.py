__all__ = ('router',)

from aiogram import Router

from .base_commands import router as commands_router
from .echo import router as echo_router

router = Router(name=__name__)

router.include_routers(
    commands_router,
    # Эхо-роутер должен быть подключен последним
    echo_router
)
