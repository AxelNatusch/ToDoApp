from src.domain.entities.todo import ToDoInDB
from src.domain.repositories.todo.todo_repository import TodoRepository


class GetTodo:
    def __init__(self, todo_repository: TodoRepository):
        self.todo_repository = todo_repository

    def get_by_id(self, todo_id: int) -> ToDoInDB | None:
        return self.todo_repository.get_by_id(todo_id)
