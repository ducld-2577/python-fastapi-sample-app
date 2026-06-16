from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.api.dependencies import (
    get_label_service,
)

from app.schemas.label import (
    LabelCreate,
    LabelUpdate,
    LabelAssignTask,
)
from app.services.label import LabelService

router = APIRouter()

LabelServiceDep = Annotated[LabelService, Depends(get_label_service)]


@router.get("/project/{project_id}", response_model=list[LabelCreate])
async def get_labels_by_project(
    project_id: int,
    service: LabelServiceDep,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
):
    return await service.get_labels_by_project(
        project_id=project_id,
        page=page,
        page_size=page_size,
    )


@router.post("/", response_model=LabelCreate)
async def create_label(
    payload: LabelCreate,
    service: LabelServiceDep,
):
    return await service.create_label(payload)


@router.put("/{label_id}", response_model=LabelUpdate)
async def update_label(
    label_id: int,
    payload: LabelUpdate,
    service: LabelServiceDep,
):
    return await service.update_label(label_id, payload)


@router.delete("/{label_id}")
async def delete_label(
    label_id: int,
    service: LabelServiceDep,
):
    await service.delete_label(label_id)
    return {"detail": "Label deleted successfully"}


@router.post("/assign-task")
async def assign_label_to_task(
    payload: LabelAssignTask,
    label_service: LabelServiceDep,
):
    return await label_service.assign_label_to_task(payload)


@router.post("/remove-task")
async def remove_label_from_task(
    payload: LabelAssignTask,
    label_service: LabelServiceDep,
):
    return await label_service.remove_label_from_task(payload)
