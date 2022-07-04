from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from codenotes.db import Base
from codenotes.db.models import AnnotationMixin
from .task import TaskModel


class CategoryModel(AnnotationMixin, Base):
    __tablename__ = "category"

    name = Column(String, nullable=False, unique=True)
    tasks = relationship(TaskModel, back_populates="category")

    def __init__(self, name: str) -> None:
        self.name = name

    def __str__(self) -> str:
        self.name
