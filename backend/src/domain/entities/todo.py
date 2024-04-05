from datetime import datetime

from pydantic import BaseModel


class ToDo(BaseModel):
    title: str
    description: str | None = None
    is_completed: bool = False


class ToDoInDB(ToDo):
    id: int
    created_at: datetime
    updated_at: datetime
