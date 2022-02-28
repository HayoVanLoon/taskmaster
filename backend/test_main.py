from dataclasses import dataclass
from typing import Dict

import pytest

import main
import models
import persistence

_FOO_ID_TOKEN = ("fakeauth.eyJlbWFpbCI6ImZvb0BleGFtcGxlLmNvbSIsImlzcyI6Imh0dHBzOi8vZmFrZWFjY291bnRz"
                 "LmV4YW1wbGUuY29tIiwic3ViIjoiZm9vQGV4YW1wbGUuY29tIn0=.lalala")
_BAR_ID_TOKEN = ("fakeauth.eyJlbWFpbCI6ImJhckBleGFtcGxlLmNvbSIsImlzcyI6Imh0dHBzOi8vZmFrZWFjY291bnRz"
                 "LmV4YW1wbGUuY29tIiwic3ViIjoiZm9vQGV4YW1wbGUuY29tIn0=.lalala")
_BLA_ID_TOKEN = ("fakeauth.eyJlbWFpbCI6ImJsYUBleGFtcGxlLmNvbSIsImlzcyI6Imh0dHBzOi8vZmFrZWFjY291bnRz"
                 "LmV4YW1wbGUuY29tIiwic3ViIjoiZm9vQGV4YW1wbGUuY29tIn0=.lalala")


@dataclass
class FakeRequest:
    headers: Dict[str, str]


@pytest.mark.asyncio
async def test_list_tasks():
    # Retrieve task lists for different users

    main.database = persistence.InMemoryPersistence()
    main.database._tasks = {
        "tasks/test1": models.Task(name="tasks/test1",
                                   owner="foo@example.com",
                                   title="title1",
                                   done=True),
        "tasks/test2": models.Task(name="tasks/test2",
                                   owner="bar@example.com",
                                   title="title2"),
        "tasks/test3": models.Task(name="tasks/test3",
                                   owner="foo@example.com",
                                   title="title3"),
    }

    # User 1: expect two tasks
    main._request = lambda: FakeRequest(headers={
        "Authorization": "Bearer " + _FOO_ID_TOKEN,
    })
    resp = await main.list_tasks()

    assert "tasks" in resp
    assert len(resp["tasks"]) == 2
    xs = sorted(resp["tasks"], key=lambda d: d["title"])
    assert xs[0]["title"] == "title1"
    assert xs[0]["done"]
    assert xs[1]["title"] == "title3"
    assert not xs[1]["done"]

    # User 2: expect one task
    main._request = lambda: FakeRequest(headers={
        "Authorization": "Bearer " + _BAR_ID_TOKEN,
    })
    resp = await main.list_tasks()

    assert "tasks" in resp
    assert len(resp["tasks"]) == 1
    assert resp["tasks"][0]["title"] == "title2"
    assert not resp["tasks"][0]["done"]

    # User 3: expect no tasks
    main._request = lambda: FakeRequest(headers={
        "Authorization": "Bearer " + _BLA_ID_TOKEN,
    })
    resp = await main.list_tasks()

    assert "tasks" in resp
    assert len(resp["tasks"]) == 0
