from sqlalchemy import Column, ForeignKey, Integer, Text

from codenotes.db.models import AnnotationMixin
from codenotes.db import Base


class TaskModel(AnnotationMixin, Base):
    __tablename__ = "task"

    content = Column(Text, nullable=False)
    category_id = Column(Integer, ForeignKey("task_category.id"))

    def __str__(self) -> str:
        return self.content
