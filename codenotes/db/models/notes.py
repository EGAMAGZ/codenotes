from sqlalchemy import Column, String, Text, Boolean, Integer, ForeignKey

from codenotes.db import Base
from codenotes.db.models import AnnotationMixin


class NoteModel(AnnotationMixin, Base):
    __tablename__ = "note"

    title = (Column(String(30), nullable=False),)
    content = Column(Text, nullable=True)
    is_markdown = Column(Boolean, nullable=False, default=False)
    category_id = Column(Integer, ForeignKey("note_category.id"))

    def __str__(self) -> str:
        return self.title
