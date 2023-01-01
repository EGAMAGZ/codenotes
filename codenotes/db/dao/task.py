import logging
from typing import List

from sqlalchemy import desc

from codenotes.db import Session
from codenotes.db.models.task import TaskModel


class TaskDao:
    """
    Dao class with all methods related to task queries.
    """
    @staticmethod
    def create(task: TaskModel) -> None:
        """
        Creates a new task.

        Parameters
        ----------
        task : TaskModel
            Task model to create a new task.
        """
        logging.info("Query executed: TaskDao.create")
        with Session.begin() as session:
            session.add(task)

    @staticmethod
    def count_tasks(category_id: int) -> int:
        """
        Counts the number of tasks in a given category.

        Parameters
        ----------
        category_id : int
            ID of the category.
        """
        logging.info("Query executed: TaskDao.count_tasks")

        with Session() as session:
            result: int = (
                session.query(TaskModel)
                .filter(TaskModel.category_id == category_id)
                .count()
            )
        return result

    @staticmethod
    def count_tasks_completed(category_id: int) -> int:
        """
        Counts the number of completed tasks in a given category.

        Parameters
        ----------
        category_id : int
            ID of the category.
        """
        logging.info("Query executed: TaskDao.count_tasks_completed")
        with Session() as session:
            result: int = (
                session.query(TaskModel)
                .filter(
                    TaskModel.completed is True,
                    TaskModel.category_id == category_id,
                )
                .count()
            )
        return result

    @staticmethod
    def get_tasks_with_limit(category_id: int, limit: int) -> List[TaskModel]:
        """
        Gets the tasks with a given limit in a given category.

        Parameters
        ----------
        category_id : int
            ID of the category.

        limit : int
            Limit number of tasks.
        """
        logging.info("Query executed: TaskDao.get_tasks_with_limit")
        with Session() as session:
            result: List[TaskModel] = (
                session.query(TaskModel)
                .filter(TaskModel.category_id == category_id)
                .order_by(desc(TaskModel.created_at))
                .limit(limit)
                .all()
            )

        return result

    @staticmethod
    def get_all_tasks(category_id: int) -> List[TaskModel]:
        """
        Gets all tasks in a given category.

        Parameters
        ----------
        category_id : int
            ID of the category.
        """
        logging.info("Query executed: TaskDao.get_all_tasks")
        with Session() as session:
            result: List[TaskModel] = (
                session.query(TaskModel)
                .filter(TaskModel.category_id == category_id)
                .order_by(desc(TaskModel.created_at))
                .all()
            )

        return result
