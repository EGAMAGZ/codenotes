from typing import List

from codenotes.db import Session
from codenotes.db.models.category import CategoryModel


class CategoryDao:
    @staticmethod
    def create(category: CategoryModel) -> None:
        with Session.begin() as session:
            session.add(category)

    @staticmethod
    def search_by_name(category_name: str) -> List[CategoryModel]:
        with Session() as session:
            result: List[CategoryModel] = (
                session.query(CategoryModel)
                .filter(CategoryModel.name.contains(category_name))
                .all()
            )
        return result

    @staticmethod
    def get_by_name(category_name: str) -> CategoryModel:
        with Session() as session:
            result: CategoryModel = (
                session.query(CategoryModel)
                .filter(CategoryModel.name == category_name)
                .one_or_none()
            )

        return result
