import logging
import functools
from typing import Callable

from fastapi import Request
from src.facades.authentication import Authentication
from src.types.exception_types import ExceptionTypes

LOGGER = logging.getLogger(__name__)


def auth() -> Callable:
    def decorator_wrapper(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            LOGGER.info("in the auth decorator")
            if "request" not in kwargs:
                raise Exception(ExceptionTypes.REQUEST_INVALID)
            request = kwargs["request"]
            assert isinstance(request, Request)

            user = Authentication().get_user(request=request)
            kwargs["user_id"] = user.id

            result = await func(*args, **kwargs)
            return result

        return wrapper

    return decorator_wrapper
