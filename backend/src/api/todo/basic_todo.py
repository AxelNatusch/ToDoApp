from typing import Annotated, List

from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, status

from src.domain.entities.todo import ToDo, ToDoInDB
from src.domain.repositories.todo.implementations.in_memory_todo_repository import (
    InMemoryTodoRepository,
)
from src.domain.repositories.todo.todo_repository import TodoRepository
from src.domain.use_cases.todo.create_todo import CreateTodo
from src.domain.use_cases.todo.delete_todo import DeleteTodo
from src.domain.use_cases.todo.get_todo import GetTodo
from src.domain.use_cases.todo.update_todo import UpdateTodo

router = APIRouter(
    prefix="/todo",
    tags=["todo"],
)

repository: TodoRepository = InMemoryTodoRepository()


# Dependency to get the todo use case instances
def get_create_todo() -> CreateTodo:
    return CreateTodo(todo_repository=repository)


def get_delete_todo() -> DeleteTodo:
    return DeleteTodo(todo_repository=repository)


def get_get_todo() -> GetTodo:
    return GetTodo(todo_repository=repository)


def get_update_todo() -> UpdateTodo:
    return UpdateTodo(todo_repository=repository)


@router.get("/{todo_id}", response_model=ToDoInDB)
async def get_todo_by_id(
    todo_id: Annotated[int, Path(description="The ID of the todo to get")],
    get_todo: Annotated[GetTodo, Depends(get_get_todo)],
) -> ToDoInDB:
    todo = get_todo.get_by_id(todo_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    return todo


@router.post("/", response_model=ToDoInDB, status_code=status.HTTP_201_CREATED)
async def create_todo_item(
    todo_data: Annotated[ToDo, Body(description="The data of the todo to create")],
    create_todo: Annotated[CreateTodo, Depends(get_create_todo)],
) -> ToDoInDB:
    return create_todo.execute(todo_data)


@router.put("/{todo_id}", response_model=ToDoInDB)
async def update_todo_item(
    todo_id: Annotated[int, Path(description="The ID of the todo to update")],
    todo_data: Annotated[ToDo, Body(description="The data of the todo to update")],
    update_todo: Annotated[UpdateTodo, Depends(get_update_todo)],
) -> ToDoInDB:
    return update_todo.execute(todo_id, todo_data)


@router.delete("/{todo_id}", response_model=bool)
async def delete_todo_item(
    todo_id: Annotated[int, Path(description="The ID of the todo to delete")],
    delete_todo: Annotated[DeleteTodo, Depends(get_delete_todo)],
) -> bool:
    success = delete_todo.execute(todo_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    return success
