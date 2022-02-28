from dataclasses import dataclass
from typing import Optional


@dataclass
class Task:

    name: str
    owner: str
    title: str
    done: bool = False

    def __post_init__(self):
        pass


Err = Optional[str]
