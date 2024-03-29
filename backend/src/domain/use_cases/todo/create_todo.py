from src.domain.entities.todo import ToDo, ToDoInDB
from src.domain.repositories.todo.todo_repository import TodoRepository


class CreateTodo:
    def __init__(self, todo_repository: TodoRepository):
        self.repository = todo_repository

    def execute(self, todo: ToDo) -> ToDoInDB:
        return self.repository.create(todo)
