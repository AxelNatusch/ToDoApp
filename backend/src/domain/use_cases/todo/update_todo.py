from src.domain.entities.todo import ToDo, ToDoInDB
from src.domain.repositories.todo.todo_repository import TodoRepository


class UpdateTodo:
    def __init__(self, todo_repository: TodoRepository):
        self.todo_repository = todo_repository

    def execute(self, todo_id: int, todo_data: ToDo) -> ToDoInDB:
        return self.todo_repository.update(todo_id, todo_data)
