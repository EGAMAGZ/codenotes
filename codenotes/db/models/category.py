from sqlalchemy import Column, String

from codenotes.db import Base
from codenotes.db.models import AnnotationMixin


class CategoryModel(AnnotationMixin, Base):
    __tablename__ = "category"

    name = Column(String, nullable=False, unique=True)
