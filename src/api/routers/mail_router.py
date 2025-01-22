import logging
from contextlib import asynccontextmanager
from typing import Optional
from fastapi import APIRouter, FastAPI, HTTPException, Request

from src.facades.email_facade import EmailFacade
from src.decorators.auth import auth
from src.types.exception_types import ExceptionTypes
from src.types.api.server_response import ServerResponse


LOGGER = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # initialize
    yield
    # cleanup


router = APIRouter(
    prefix=f"/mail",
    tags=["mail"],
    lifespan=lifespan,
)


@router.post("/send-mail")
@auth()
async def send_mail(
    email: str, title: str, body: str, request: Request, user_id: Optional[str] = None
) -> ServerResponse:
    if not user_id:
        raise HTTPException(401, ExceptionTypes.AUTH_REQUIRED.value)
    EmailFacade().send(email, title, body)
    return ServerResponse()
