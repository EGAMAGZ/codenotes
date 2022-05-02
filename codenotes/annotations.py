from enum import Enum


class Annotations(Enum):
    TASK = 1
    NOTE = 2

    @classmethod
    def list_names(cls) -> list[str]:
        m = map(lambda c: c.name, cls)
        return list(m)
