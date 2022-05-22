from codenotes.db import Session
from codenotes.db.models.category import CategoryModel


class CategoryDao:
    def create(self, category: CategoryModel) -> None:
        with Session.begin() as session:
            session.add(category)
