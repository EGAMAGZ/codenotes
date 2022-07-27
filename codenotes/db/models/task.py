from sqlalchemy import Column, String, Integer, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship

from codenotes.db import Base
from codenotes.db.models import AnnotationMixin


class TaskModel(AnnotationMixin, Base):
    __tablename__ = 'task'

    content = Column(String, nullable=False)
    completed_at = Column(Date, nullable=True)
    completed = Column(Boolean, default=False)

    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship("CategoryModel", back_populates="tasks")

    def __init__(self, content: str, category) -> None:
        self.content = content
        self.category = category
