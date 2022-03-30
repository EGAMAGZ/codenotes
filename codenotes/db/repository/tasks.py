from codenotes.db import Session
from codenotes.db.models.tasks import TaskModel
from codenotes.db.repository import BaseRepository


class TaskRepository(BaseRepository):
    def add(self, value: TaskModel) -> None:
        with Session() as session, session.begin():
            session.add(value)

    def add_all(self, value: list[TaskModel]) -> None:
        with Session() as session, session.begin():
            session.add_all(value)

    def get(self, id: int) -> TaskModel:
        pass

    def delete(self, value: TaskModel) -> None:
        pass

    def list(self) -> list[TaskModel]:
        pass
