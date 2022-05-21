from datetime import datetime

from sqlalchemy import Column, Integer, DateTime


class AnnotationMixin:
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.now())
