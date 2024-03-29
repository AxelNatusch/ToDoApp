from src.domain.repositories.todo.todo_repository import TodoRepository


class DeleteTodo:
    def __init__(self, todo_repository: TodoRepository):
        self.todo_repository = todo_repository

    def execute(self, todo_id: int) -> None:
        self.todo_repository.delete_by_id(todo_id)
