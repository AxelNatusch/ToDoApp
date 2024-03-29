from typing import Annotated

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

# here we choose the actual repository implementation to use
# in this case, we are using an in-memory repository implementation so we can test the API without the need of a database
# this can be easily changed to use a database repository implementation without changing the rest of the code
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


@router.get("/{todo_id}", response_model=ToDoInDB, status_code=status.HTTP_200_OK)
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


@router.put("/{todo_id}", response_model=ToDoInDB, status_code=status.HTTP_200_OK)
async def update_todo_item(
    todo_id: Annotated[int, Path(description="The ID of the todo to update")],
    todo_data: Annotated[ToDo, Body(description="The data of the todo to update")],
    update_todo: Annotated[UpdateTodo, Depends(get_update_todo)],
) -> ToDoInDB:
    try:
        return update_todo.update_by_id(todo_id, todo_data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{todo_id}", response_model=bool, status_code=status.HTTP_200_OK)
async def delete_todo_item(
    todo_id: Annotated[int, Path(description="The ID of the todo to delete")],
    delete_todo: Annotated[DeleteTodo, Depends(get_delete_todo)],
) -> bool:
    success = delete_todo.delete_by_id(todo_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    return success
