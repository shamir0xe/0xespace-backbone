import logging
from contextlib import asynccontextmanager
from typing import Optional
from fastapi import APIRouter, FastAPI, HTTPException, Request
from pylib_0xe.config.config import Config

from src.facades.email_facade import EmailFacade
from src.decorators.auth import auth
from src.types.exception_types import ExceptionTypes
from src.types.api.server_response import ServerResponse
from src.types.email_templates import EmailTemplates


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


@router.post("/send-verification")
@auth()
async def send_verification(
    email: str,
    code: str,
    reciepant_id: str,
    reciepant_username: str,
    request: Request,
    user_id: Optional[str] = None,
):
    if not user_id:
        raise HTTPException(401, ExceptionTypes.AUTH_REQUIRED.value)
    title = Config.read("email.verification.title")
    body = EmailFacade().create_template(
        EmailTemplates.VERIFICATION,
        code=code,
        user_id=reciepant_id,
        username=reciepant_username,
    )
    EmailFacade().send(email, title, body)
    return ServerResponse()
