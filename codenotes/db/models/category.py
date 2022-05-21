from sqlalchemy import Column, String, Enum

from codenotes import Annotations
from codenotes.db import Base
from codenotes.db.models import AnnotationMixin


class CategoryModel(AnnotationMixin, Base):
    name = Column(String, nullable=False, unique=True)
    annotation_type = Column(Enum(Annotations), nullable=False)

    def __str__(self) -> str:
        return self.name
