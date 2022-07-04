import logging
from typing import List

from codenotes.db import Session
from codenotes.db.models.category import CategoryModel


class CategoryDao:
    """
    Dao class with all methods related to category queries.
    """

    @staticmethod
    def create(category: CategoryModel) -> None:
        """
        Creates a new category.

        Parameters
        ----------
        category : CategoryModel
            Category model to create a category.
        """
        logging.info("Query executed: CategoryDao.create")
        with Session.begin() as session:
            session.add(category)

    @staticmethod
    def search_by_name(category_name: str) -> List[CategoryModel]:
        """
        Search for all categories that contains the given category name. Each
        category from the list only contains its name.

        Parameters
        ----------
        category_name : str
            Name of the category that will be searched.
        Returns
        -------
        result : List[CategoryModel]
            List of categories that contains the specified category name.
        """
        logging.info("Query executed: CategoryDao.search_by_name")
        with Session() as session:
            result: List[CategoryModel] = (
                session.query(CategoryModel.name)
                .filter(CategoryModel.name.contains(category_name))
                .all()
            )
        return result


def get_by_name(category_name: str) -> CategoryModel:
    """
    Gets a single category by its name. In case it is not found, returns None.

    Parameters
    ----------
    category_name : str
        Name of the category that will be searched.

    Returns
    -------
    category: CategoryModel
        Category that might have been found by the search.
    """
    logging.info("Query executed: CategoryDao.get_by_name")
    with Session() as session:
        result: CategoryModel = (
            session.query(CategoryModel)
            .filter(CategoryModel.name == category_name)
            .one_or_none()
        )
    return result
