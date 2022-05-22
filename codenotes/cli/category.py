from typing import Tuple

from codenotes import Annotations
from codenotes.db.dao.category import CategoryDao
from codenotes.db.models.category import CategoryModel
from codenotes.utils.text import tuple_to_str


class CreateCategory:
    dao: CategoryDao
    category_name: str
    annotation_type: int
    preview: bool

    def __init__(self, category_name: Tuple[str], annotation_name: str, preview: bool):
        self.dao = CategoryDao()
        self.category_name = tuple_to_str(category_name)
        self.annotation_type = Annotations.get_value_by_key(annotation_name)
        self.preview = preview

        self.dao.create(
            CategoryModel(
                name=self.category_name,
                annotation_type=self.annotation_type
            )
        )
