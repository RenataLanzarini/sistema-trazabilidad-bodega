from typing import Annotated, Any

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.core.security import decode_access_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)


def get_current_user_payload(
    token: Annotated[str | None, Depends(oauth2_scheme)],
) -> dict[str, Any]:
    if token is None:
        from app.core.exceptions import UnauthorizedError

        raise UnauthorizedError("Credenciales de autenticacion requeridas.")
    return decode_access_token(token)
