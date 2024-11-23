from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.users import User
from common.jwt.jwt import decode_access_token, SUB
from db.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        db: AsyncSession = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = await decode_access_token(token, db=db)
        user = await User.find_by_id(db=db, id=payload[SUB])
        if user is None:
            raise credentials_exception
    except (JWTError, ValidationError):
        raise credentials_exception
    return user
