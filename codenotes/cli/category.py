from codenotes import Annotations


class CreateCategory:
    category_name: str
    annotation_type: int
    preview: bool

    def __init__(self, category_name: str, annotation_name: str, preview: bool):
        self.category_name = category_name
        self.annotation_type = Annotations.get_value_by_key(annotation_name)
        self.preview = preview
