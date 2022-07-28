import logging
from typing import List

from codenotes.db import Session
from codenotes.db.models.task import TaskModel


class TaskDao:
    @staticmethod
    def create(task: TaskModel) -> None:
        logging.info("Query executed: TaskDao.create")
        with Session.begin() as session:
            session.add(task)

    @staticmethod
    def count_tasks(category_id: int) -> int:
        with Session() as session:
            result: int = session.query(TaskModel).filter(
                TaskModel.category_id == category_id).count()
        return result

    @staticmethod
    def count_tasks_completed(category_id: int,
                              completed: bool = True) -> int:
        with Session() as session:
            result: int = session.query(TaskModel).filter(
                TaskModel.completed is completed,
                TaskModel.category_id == category_id
            ).count()
        return result

    @staticmethod
    def get_tasks_with_limit(category_id: int, limit: int) -> List[TaskModel]:
        with Session() as session:
            # TODO: ADD FEATURE TO ORDER BY DATE IN ASCENDING ORDER OR BY
            #  DESCENDING ORDER
            result: List[TaskModel] = session.query(TaskModel).filter(
                TaskModel.category_id == category_id).limit(limit).all()

        return result
