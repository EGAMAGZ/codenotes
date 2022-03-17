from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from codenotes.db.models import AnnotationMixin
from codenotes.db import Base


class TaskCategoryModel(AnnotationMixin, Base):
    __tablename__ = "task_category"

    name = Column(String(30), nullable=False, unique=True)
    tasks = relationship("TaskModel", backref="task_category")

    def __str__(self) -> str:
        return self.name


class TaskModel(AnnotationMixin, Base):
    __tablename__ = "task"

    content = Column(Text, nullable=False)
    category_id = Column(Integer, ForeignKey("task_category.id"))

    def __str__(self) -> str:
        return self.content
