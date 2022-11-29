import asyncio
import json
from typing import Optional, Callable

from fastapi import Depends, status
from fastapi import HTTPException, Query
from jose import jwt, JWTError
from sqlalchemy import asc, desc
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import DeclarativeMeta

from backend.app import crud, models, schemas
from backend.app.core.config import settings
from backend.app.core.security import oauth2Scheme
from backend.app.db.session import AsyncSessionLocal
from backend.app.models.user import User
from backend.app.schemas.request_params import RequestParams

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


async def get_async_session():
    session: AsyncSession = AsyncSessionLocal()
    try:
        session.current_user_id = None
        yield session
    finally:
        await session.close()


async def get_current_user_async(
        db: AsyncSession = Depends(get_async_session),
        token: str = Depends(oauth2Scheme)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False},
        )
        subject: str = payload.get("sub")
        scopes: str = payload.get("scopes")
        if not subject:
            raise credentials_exception
        token_data = schemas.TokenPayload(sub=subject, scopes=scopes)
    except JWTError:
        raise credentials_exception
    if not token_data.sub.isdigit():
        raise credentials_exception
    user = await crud.user.get_by_id(db=db, id=int(token_data.sub))
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
        current_user: models.User = Depends(get_current_user_async),
) -> models.User:
    if not crud.user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_active_superuser(
        current_user: User = Depends(get_current_user_async),
) -> User:
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user


def parse_react_admin_params(model: DeclarativeMeta) -> Callable[[str | None, str | None], RequestParams]:
    """Parses sort and range parameters coming from a react-admin request"""

    def inner(
            sort_: Optional[str] = Query(
                None,
                alias="sort",
                description='Format: `["field_name", "direction"]`',
                example='["id", "ASC"]',
            ),
            range_: Optional[str] = Query(
                None,
                alias="range",
                description="Format: `[start, end]`",
                example="[0, 10]",
            ),
    ):
        skip, limit = 0, 10
        if range_:
            start, end = json.loads(range_)
            skip, limit = start, (end - start + 1)

        order_by = desc(model.id) # noqa
        if sort_:
            sort_column, sort_order = json.loads(sort_)
            if sort_order.lower() == "asc":
                direction = asc
            elif sort_order.lower() == "desc":
                direction = desc
            else:
                raise HTTPException(400, f"Invalid sort direction {sort_order}")
            order_by = direction(model.__table__.c[sort_column]) # noqa

        return RequestParams(skip=skip, limit=limit, order_by=order_by)

    return inner
