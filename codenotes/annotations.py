from enum import Enum


class Annotations(Enum):
    TASK = 1
    NOTE = 2

    @classmethod
    def list_names(cls) -> list[str]:
        return [annotation.name for annotation in cls]
