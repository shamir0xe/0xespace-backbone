import logging
from contextlib import asynccontextmanager
from fastapi import APIRouter, FastAPI, HTTPException
from pylib_0xe.database.actions.release_session import ReleaseSession
from pylib_0xe.types.database_types import DatabaseTypes

from src.actions.auth.check_token_expired import CheckTokenExpired
from src.facades.password_facade import PasswordFacade
from src.models.token import Token
from src.models.user import User
from src.repositories.user_repository import UserRepository

LOGGER = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # initialize
    yield
    # cleanup


router = APIRouter(
    prefix=f"/auth",
    tags=["auth"],
    lifespan=lifespan,
)


@router.post("/login")
async def login(username: str, password: str) -> str:
    user, session = UserRepository(User).read_by_username(
        username, db_session_keep_alive=True
    )
    if PasswordFacade.verify_password(password, user.password):
        if not user.token or CheckTokenExpired(user.token).check():
            user.token = Token()
            session.add(user)
    else:
        ReleaseSession(DatabaseTypes.I, session).release()
        # Modify returning message
        message = "Username and password do not match"
        raise HTTPException(401, message)
    session.commit()
    ReleaseSession(DatabaseTypes.I, session).release()
    return user.token.id
