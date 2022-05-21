from enum import Enum


class Annotations(Enum):
    TASK = 1
    NOTE = 2

    @classmethod
    def list_names(cls) -> list[str]:
        return [annotation.name for annotation in cls]

    @classmethod
    def get_value_by_key(cls, key: str) -> int:
        try:
            enum_key = key.upper()
            return cls[enum_key].value
        except KeyError:
            return -1
