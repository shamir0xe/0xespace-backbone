from datetime import UTC, datetime
import logging
from contextlib import asynccontextmanager
from typing import Optional
from fastapi import APIRouter, FastAPI, HTTPException, Request
from pylib_0xe.database.actions.release_session import ReleaseSession
from pylib_0xe.types.database_types import DatabaseTypes

from src.models.user import User
from src.repositories.repository import Repository
from src.decorators.auth import auth
from src.types.exception_types import ExceptionTypes
from src.types.api.ping_response import PingResponse


LOGGER = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # initialize
    yield
    # cleanup


router = APIRouter(
    prefix=f"/utils",
    tags=["utils"],
    lifespan=lifespan,
)


@router.post("/ping")
@auth()
async def ping(request: Request, user_id: Optional[str] = None) -> PingResponse:
    if not user_id:
        raise HTTPException(401, ExceptionTypes.AUTH_REQUIRED.value)
    user, session = Repository(User).read_by_id(user_id, db_session_keep_ailve=True)
    try:
        response = PingResponse(
            remaining_time=round(
                (
                    datetime.now(UTC) - user.token.updated_at.replace(tzinfo=UTC)
                ).total_seconds()
            )
        )
    except Exception as e:
        ReleaseSession(DatabaseTypes.I, session).release()
        raise HTTPException(500, f"Cannot access ping result {str(e)}")
    ReleaseSession(DatabaseTypes.I, session).release()
    return response
