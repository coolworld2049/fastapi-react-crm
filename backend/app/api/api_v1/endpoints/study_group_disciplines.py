from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app import crud, schemas
from backend.app.api import deps
from backend.app.db import models
from backend.app.schemas.request_params import RequestParams

router = APIRouter()


# noinspection PyUnusedLocal
@router.get("/", response_model=List[schemas.StudyGroupDiscipline])
async def read_study_group_discipline(
        response: Response,
        db: AsyncSession = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
        request_params: RequestParams = Depends(deps.parse_react_admin_params(models.StudyGroupDiscipline))
) -> Any:
    """
    Retrieve StudyGroupDisciplines.
    """
    items, total = await crud.study_group_discipline.get_multi(db, request_params=request_params)
    response.headers["Content-Range"] = f"{request_params.skip}-{request_params.skip + len(items)}/{total}"
    return items


# noinspection PyUnusedLocal
@router.put("/{id}", response_model=schemas.StudyGroupDiscipline)
async def update_study_group_discipline_id(
        *,
        db: AsyncSession = Depends(deps.get_db),
        id: int,
        item_in: schemas.StudyGroupDisciplineUpdate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an StudyGroupDiscipline.
    """
    item = await crud.study_group_discipline.get(db=db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item = await crud.study_group_discipline.update(db=db, db_obj=item, obj_in=item_in)
    return item


# noinspection PyUnusedLocal
@router.get("/{id}", response_model=schemas.StudyGroupDiscipline)
async def read_study_group_discipline_id(
        *,
        db: AsyncSession = Depends(deps.get_db),
        id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get StudyGroupDiscipline by ID.
    """
    item = await crud.study_group_discipline.get(db=db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


# noinspection PyUnusedLocal
@router.delete("/{id}", response_model=schemas.StudyGroupDiscipline)
async def delete_study_group_discipline_id(
        *,
        db: AsyncSession = Depends(deps.get_db),
        id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an StudyGroupDiscipline.
    """
    item = await crud.study_group_discipline.get(db=db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item = await crud.study_group_discipline.remove(db=db, id=id)
    return item
