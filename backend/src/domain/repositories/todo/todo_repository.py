from abc import ABC, abstractmethod

from src.domain.entities.todo import ToDo, ToDoInDB


class TodoRepository(ABC):
    """
    Interface for the TodoRepository class
    - used to define the methods that the TodoRepository class should implement
    - all implementations of the TodoRepository class should inherit from this class
    """

    @abstractmethod
    def create(self, todo: ToDo) -> ToDoInDB:
        pass

    @abstractmethod
    def update_by_id(self, todo_id: int, todo_data: ToDo) -> ToDoInDB:
        pass

    @abstractmethod
    def delete_by_id(self, todo_id: int) -> bool:
        pass

    @abstractmethod
    def get_by_id(self, todo_id: int) -> ToDoInDB | None:
        pass
