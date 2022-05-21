from sqlalchemy import Column, String, Integer

from codenotes.db import Base
from codenotes.db.models import AnnotationMixin


class CategoryModel(AnnotationMixin, Base):
    __tablename__ = "category"

    name = Column(String, nullable=False, unique=True)
    annotation_type = Column(Integer, nullable=False)

    def __str__(self) -> str:
        return self.name
