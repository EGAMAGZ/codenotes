from typing import List

from codenotes.db import Session
from codenotes.db.models.category import CategoryModel


class CategoryDao:
    def create(self, category: CategoryModel) -> None:
        with Session.begin() as session:
            session.add(category)

    def get_by_name(self, category_name: str) -> List[CategoryModel]:
        with Session() as session:
            result: List[CategoryModel] = (
                session.query(CategoryModel)
                .filter(CategoryModel.name.contains(category_name))
                .all()
            )
        return result
