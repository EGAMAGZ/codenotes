from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from codenotes.db import Base
from codenotes.db.models import AnnotationMixin


class NoteCategoryModel(AnnotationMixin, Base):
    __tablename__ = "note_category"

    name = Column(String(30), nullable=False, unique=True)
    notes = relationship("NoteModel", backref="note_category")

    def __str__(self) -> str:
        return self.name


class TaskCategoryModel(AnnotationMixin, Base):
    __tablename__ = "task_category"

    name = Column(String(30), nullable=False, unique=True)
    tasks = relationship("TaskModel", backref="task_category")

    def __str__(self) -> str:
        return self.name
