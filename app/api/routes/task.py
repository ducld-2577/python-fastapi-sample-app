from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.dependencies import (
    get_task_service,
)

from app.schemas.task import (
    TaskAssign,
    TaskCreate,
    TaskRead,
    TaskUpdate,
    TaskUpdatePriority,
    TaskUpdateStatus,
)
from app.services.task import TaskService

router = APIRouter()

TaskServiceDep = Annotated[TaskService, Depends(get_task_service)]


@router.get("/project/{project_id}", response_model=list[TaskRead])
async def get_tasks_by_project(
    project_id: int,
    service: TaskServiceDep,
):
    return await service.get_tasks_by_project(project_id)


@router.get("/assignee/{assignee_id}", response_model=list[TaskRead])
async def get_tasks_by_assignee(
    assignee_id: int,
    service: TaskServiceDep,
):
    return await service.get_tasks_by_assignee(assignee_id)


@router.get("/{task_id}", response_model=TaskRead)
async def get_task_by_id(
    task_id: int,
    service: TaskServiceDep,
):
    return await service.get_task(task_id)


@router.post("/", response_model=TaskRead)
async def create_task(
    payload: TaskCreate,
    service: TaskServiceDep,
):
    return await service.create_task(payload)


@router.put("/{task_id}/status", response_model=TaskRead)
async def update_task_status(
    task_id: int,
    payload: TaskUpdateStatus,
    service: TaskServiceDep,
):
    return await service.update_task_status(task_id, payload)


@router.put("/{task_id}/priority", response_model=TaskRead)
async def update_task_priority(
    task_id: int,
    payload: TaskUpdatePriority,
    service: TaskServiceDep,
):
    return await service.update_task_priority(task_id, payload)


@router.put("/{task_id}/assignee", response_model=TaskRead)
async def update_task_assignee(
    task_id: int,
    payload: TaskAssign,
    service: TaskServiceDep,
):
    return await service.assign_task(task_id, payload)


@router.put("/{task_id}", response_model=TaskRead)
async def update_task(
    task_id: int,
    payload: TaskUpdate,
    service: TaskServiceDep,
):
    return await service.update_task(task_id, payload)


@router.delete("/{task_id}", status_code=204)
async def delete_task(
    task_id: int,
    service: TaskServiceDep,
):
    await service.delete_task(task_id)
