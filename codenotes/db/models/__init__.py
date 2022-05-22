from datetime import date

from sqlalchemy import Column, Integer, Date


class AnnotationMixin:
    id = Column(Integer, primary_key=True)
    created_at = Column(Date, default=date.today())
