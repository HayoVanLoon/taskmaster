import abc
from typing import Dict, List, Optional, Tuple

import models


class Persistence(abc.ABC):

    def fetch_tasks(self) -> Tuple[List[models.Task], models.Err]:
        pass

    def fetch_task(self, name: str) -> Tuple[Optional[models.Task], models.Err]:
        pass

    def save_task(self, task: models.Task) -> models.Err:
        pass


class InMemoryPersistence(Persistence):

    def __init__(self) -> None:
        super().__init__()
        self._tasks: Dict[str, models.Task] = {}

    def fetch_tasks(self) -> Tuple[List[models.Task], models.Err]:
        return list(self._tasks.values()), None

    def fetch_task(self, name: str) -> Tuple[Optional[models.Task], models.Err]:
        return self._tasks.get(name), None

    def save_task(self, task: models.Task) -> models.Err:
        self._tasks[task.name] = task
        return None


class FirestorePersistence(Persistence):
    # TODO(hvl): implement...

    def __init__(self) -> None:
        super().__init__()

    def fetch_tasks(self) -> Tuple[List[models.Task], models.Err]:
        pass

    def fetch_task(self, name: str) -> Tuple[Optional[models.Task], models.Err]:
        pass

    def save_task(self, task: models.Task) -> models.Err:
        pass


_INSTANCE: Optional[Persistence] = None


def get_instance() -> Tuple[Persistence, models.Err]:
    global _INSTANCE
    if not _INSTANCE:
        # TODO(hvl): switch to FirestorePersistence once implemented
        _INSTANCE = InMemoryPersistence()
    return _INSTANCE, None
