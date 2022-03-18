from typing import Any

from sqlalchemy.orm import Session

from codenotes.db.models.tasks import TaskModel
from codenotes.db.repository import BaseRepository


class TaskRepository(BaseRepository):

    def __init__(self, session: Session):
        super().__init__(session)

    def add(self, value: TaskModel) -> None:
        with self.session.begin() as session:
            session.add(value)
            session.commit()

    def add_all(self, value: list[TaskModel]) -> None:
        pass

    def get(self, id: int) -> TaskModel:
        pass

    def delete(self, value: TaskModel) -> None:
        pass

    def list(self) -> list[TaskModel]:
        pass

