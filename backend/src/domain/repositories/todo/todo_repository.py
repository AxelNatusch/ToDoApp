from abc import ABC, abstractmethod

from src.domain.entities.todo import ToDo, ToDoInDB


class TodoRepository(ABC):
    @abstractmethod
    def create(self, todo: ToDo) -> ToDoInDB:
        pass

    @abstractmethod
    def update(self, todo_id: int, todo_data: ToDo) -> ToDoInDB:
        pass

    @abstractmethod
    def delete_by_id(self, todo_id: int) -> bool:
        pass

    @abstractmethod
    def get_by_id(self, todo_id: int) -> ToDoInDB | None:
        pass
