from datetime import datetime
from typing import Dict

from src.domain.entities.todo import ToDo, ToDoInDB
from src.domain.repositories.todo.todo_repository import TodoRepository


class InMemoryTodoRepository(TodoRepository):
    def __init__(self):
        self.todos: Dict[int, ToDoInDB] = {}
        self._id_counter: int = 1

    def create(self, todo: ToDo) -> ToDoInDB:
        todo_in_db = ToDoInDB(
            id=self._id_counter,
            title=todo.title,
            description=todo.description,
            is_completed=todo.is_completed,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        self.todos[self._id_counter] = todo_in_db
        self._id_counter += 1
        return todo_in_db

    def update_by_id(self, todo_id: int, todo_data: ToDo) -> ToDoInDB:
        todo_in_db = self.todos.get(todo_id, None)
        if todo_in_db:
            todo_in_db.title = todo_data.title or todo_in_db.title
            todo_in_db.description = todo_data.description or todo_in_db.description
            todo_in_db.is_completed = todo_data.is_completed or todo_in_db.is_completed
            todo_in_db.updated_at = datetime.now()
            return todo_in_db

        else:
            raise ValueError(f"Todo with ID {todo_id} not found")

    def delete_by_id(self, todo_id: int) -> bool:
        if todo_id in self.todos:
            del self.todos[todo_id]
            return True
        return False

    def get_by_id(self, todo_id: int) -> ToDoInDB | None:
        return self.todos.get(todo_id, None)
