import base64
import json
import logging
import os
import uuid
from typing import Any, Dict, List, Optional, Tuple, Union

import flask
import flask_cors
from flask import Flask, request

import models
import persistence

logging.basicConfig(level=logging.INFO)

app = Flask("my_app")
flask_cors.CORS(app)

database: Optional[persistence.Persistence] = None


@app.route("/tasks", methods=["GET"])
async def list_tasks():
    owner, err = _get_owner(_request())
    if err:
        # TODO(hvl): return 401 or 403 once real authentication is implemented
        logging.info("error getting user from header: %s, using fallback", err)
        owner = "johndoe@example.com"

    tasks, err = database.fetch_tasks()
    if err:
        logging.warning("error fetching tasks: %s", err)
        return "could not fetch tasks", 500

    owned = [task.__dict__ for task in tasks if task.owner == owner]

    return {"tasks": owned}


@app.route("/tasks", methods=["POST"])
async def create_task():
    owner, err = _get_owner(_request())
    if err:
        # TODO(hvl): return 401 or 403 once real authentication is implemented
        logging.info("error getting user from header: %s, using fallback", err)
        owner = "johndoe@example.com"

    req = _get_json()
    err = _validate_create_task(req)
    if err:
        return err, 400

    task = models.Task(name="tasks/" + str(uuid.uuid4()),
                       owner=owner,
                       title=req["task"]["title"])

    err = database.save_task(task)
    if err:
        logging.warning("error saving task: %s", err)
        return "could not create task", 500

    return task.__dict__


@app.route("/tasks/<id_>", methods=["GET"])
async def get_task(id_: str):
    owner, err = _get_owner(_request())
    if err:
        # TODO(hvl): return 401 or 403 once real authentication is implemented
        logging.info("error getting user from header: %s, using fallback", err)
        owner = "johndoe@example.com"

    name = "tasks/" + id_
    task, err = database.fetch_task(name=name)
    if err:
        logging.warning("error fetching task: %s", err)
        return "could not fetch task", 500
    if not task:
        return "not found", 404
    if task.owner != owner:
        return "not found", 404

    return task.__dict__


@app.route("/tasks/<id_>", methods=["POST", "PATCH"])
async def update_task(id_: str):
    owner, err = _get_owner(_request())
    if err:
        # TODO(hvl): return 401 or 403 once real authentication is implemented
        logging.info("error getting user from header: %s, using fallback", err)
        owner = "johndoe@example.com"

    name = "tasks/" + id_
    data = _get_json()
    if not data:
        return "missing task", 400

    task, err = database.fetch_task(name)
    if err:
        logging.warning("error fetching task: %s", err)
        return "error updating task", 500
    if not task:
        return f"task {name} does not exist", 404
    if owner != task.owner:
        # hvl: leave them none-the-wiser
        return f"task {name} does not exist", 404

    for k, v in data.items():
        if k == "title":
            task.title = v
        elif k == "done":
            task.done = v

    err = database.save_task(task)
    if err:
        logging.warning("error saving task: %s", err)
        return "could not update task", 500
    return task.__dict__


def _validate_create_task(req: Dict[str, Any]) -> models.Err:
    if not req:
        return "no message body"
    task_data = req.get("task")
    if not task_data:
        return "missing task"
    title = task_data.get("title")
    if not title:
        return "missing title"


def _get_json() -> Optional[Union[Dict[str, Any], List[Any]]]:
    """Tries to retrieve the request body as json. Also works when content type
    header has not been set properly.

    Returns:
        The parsed json message (if present)
    """
    data = request.json
    if data:
        return data
    raw = request.data
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return None


def _get_owner(req) -> Tuple[Optional[str], models.Err]:
    """Retrieves the user from the Authorization header

    Args:
        req: Flask request

    Returns:
        The email address in the token or an error
    """
    auth = req.headers.get("Authorization")
    if not auth:
        return None, "no Authorization header provided"
    if auth[:7] != "Bearer ":
        return None, "not an identity token"
    parts = auth[7:].split(".")
    if len(parts) != 3:
        return None, "not an identity token"
    try:
        padded = parts[1] + "=" * (len(parts[1]) % 4)
        decoded = base64.b64decode(padded)
        payload = json.loads(decoded)
        return payload.get("email"), None
    except json.JSONDecodeError:
        return None, "could not decode payload as json"


def _request() -> flask.Request:
    """Wrapper function for simplifying unit testing.

    Returns:
        the Flask request
    """
    return request


def main():
    global database
    database, err = persistence.get_instance()
    if err:
        logging.error("error initialising persistence: %s", err)
        exit(3)
    return app


if __name__ == "__main__":
    main().run(port=os.getenv("PORT", 8080), debug=True)
