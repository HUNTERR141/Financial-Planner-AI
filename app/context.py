from contextlib import contextmanager
from contextvars import ContextVar
from typing import Iterator, Optional

DEFAULT_LOCAL_USER_ID = "local-user"
_current_user_id: ContextVar[Optional[str]] = ContextVar("current_user_id", default=DEFAULT_LOCAL_USER_ID)


def get_current_user_id() -> str:
    return _current_user_id.get() or DEFAULT_LOCAL_USER_ID


@contextmanager
def user_context(user_id: str | None) -> Iterator[None]:
    token = _current_user_id.set(user_id or DEFAULT_LOCAL_USER_ID)
    try:
        yield
    finally:
        _current_user_id.reset(token)
