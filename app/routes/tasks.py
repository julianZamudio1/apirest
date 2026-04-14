from fastapi import APIRouter, HTTPException, status, Depends
from app.db.mongodb import tasks_collection
from app.schemas.task import TaskCreate, TaskResponse
from app.db.utils import fix_id
from typing import List
from bson import ObjectId
from app.db.auth import get_current_user

router = APIRouter(prefix="/tasks", tags=["Tareas"])

#post
@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate, current_user: str = Depends(get_current_user)):
    task_dict = task.model_dump()
    new_task = await tasks_collection.insert_one(task_dict)
    created_task = await tasks_collection.find_one({"_id": new_task.inserted_id})
    print(f"Tarea creada: {current_user} - {created_task}")
    return fix_id(created_task)

#get
@router.get("/", response_model=List[TaskResponse])
async def get_tasks():
    tasks = []
    async for task in tasks_collection.find():
        tasks.append(fix_id(task))
    return tasks

#get by id
@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: str):
    task = await tasks_collection.find_one({"_id": task_id})
    try:
        task = await tasks_collection.find_one({"_id": ObjectId(task_id)})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID de tarea no válido")
    if task:
        return fix_id(task)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")

#put
@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(task_id: str, task: TaskCreate):
    try:
        updated_task = await tasks_collection.find_one_and_update(
            {"_id": ObjectId(task_id)},
            {"$set": task.model_dump()},
            return_document=True
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID de tarea no válido")
    if updated_task:
        return fix_id(updated_task)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")

#delete
@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: str):
    try:
        result = await tasks_collection.delete_one({"_id": ObjectId(task_id)})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID de tarea no válido")
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")
    return None

