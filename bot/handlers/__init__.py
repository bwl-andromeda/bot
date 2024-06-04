from . import help, start, profile
from aiogram import Router

__all__ = ('help', 'start', 'setup_routers')


def setup_routers() -> Router:
    router = Router()
    router.include_router(help.router)
    router.include_router(start.router)
    router.include_router(profile.router)

    return router
