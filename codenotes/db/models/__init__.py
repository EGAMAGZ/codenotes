from datetime import datetime

from sqlalchemy import Column, DateTime, Integer


class AnnotationMixin(object):

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.now())
