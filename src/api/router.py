import logging
from contextlib import asynccontextmanager
from fastapi import APIRouter, FastAPI
from pylib_0xe.config.config import Config

from src.orchestrators.initialize import Initialize
from .routers.mail_router import router as mail_router
from .routers.auth_router import router as auth_router
from .routers.utils_router import router as utils_router

version = Config.read("api.version")

LOGGER = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # initialize
    LOGGER.info(f"in the lifespan of the main router")
    Initialize()
    yield
    LOGGER.info(f"Cleanup")


router = APIRouter(
    prefix=f"/v{version}",
    lifespan=lifespan,
    responses={404: {"description": "Not found"}},
)

router.include_router(auth_router)
router.include_router(mail_router)
router.include_router(utils_router)

