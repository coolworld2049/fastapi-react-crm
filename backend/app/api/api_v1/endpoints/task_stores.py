from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession


from backend.app import crud, schemas
from backend.app.api import deps
from backend.app.db import models
from backend.app.schemas.request_params import RequestParams

router = APIRouter()


# noinspection PyUnusedLocal
@router.get("/", response_model=List[schemas.TaskStore])
async def read_task_stores(
        response: Response,
        db: AsyncSession = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
        request_params: RequestParams = Depends(deps.parse_react_admin_params(models.TaskStore))
) -> Any:
    """
    Retrieve TaskStores.
    """
    items, total = await crud.task_store.get_multi(db, request_params=request_params)
    response.headers["Content-Range"] = f"{request_params.skip}-{request_params.skip + len(items)}/{total}"
    return items


# noinspection PyUnusedLocal
@router.post("/", response_model=schemas.TaskStore)
async def create_task_store(
        *,
        db: AsyncSession = Depends(deps.get_db),
        item_in: schemas.TaskStoreCreate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new task_store.
    """
    item = await crud.task_store.create(db=db, obj_in=item_in)
    return item


# noinspection PyUnusedLocal
@router.put("/{id}", response_model=schemas.TaskStore)
async def update_task_store(
        *,
        db: AsyncSession = Depends(deps.get_db),
        id: int,
        item_in: schemas.TaskStoreUpdate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an task_store.
    """
    item = await crud.task_store.get(db=db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item = await crud.task_store.update(db=db, db_obj=item, obj_in=item_in)
    return item


# noinspection PyUnusedLocal
@router.get("/{id}", response_model=schemas.TaskStore)
async def read_task_store(
        *,
        db: AsyncSession = Depends(deps.get_db),
        id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get task_store by ID.
    """
    item = await crud.task_store.get(db=db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


# noinspection PyUnusedLocal
@router.delete("/{id}", response_model=schemas.TaskStore)
async def delete_task_store(
        *,
        db: AsyncSession = Depends(deps.get_db),
        id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an task_store.
    """
    item = await crud.task_store.get(db=db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item = await crud.task_store.remove(db=db, id=id)
    return item
