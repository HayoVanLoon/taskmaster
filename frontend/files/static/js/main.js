'use strict';

(function () {

  const API_TARGET = "${API_TARGET}";

  const CURRENT_USER_INPUT = document.getElementById("current-user-input");
  const REFRESH_USER_BUTTON = document.getElementById("refresh-user-button");

  const TASKS_LIST = document.getElementById("tasks-list");
  const CREATE_TASK_BUTTON = document.getElementById("create-task-button");

  const TITLE_INPUT = document.getElementById("title-input");
  const DONE_INPUT = document.getElementById("done-input");
  const SAVE_TASK_BUTTON = document.getElementById("save-task-button");

  const MESSAGE_DIV = document.getElementById("message-div");
  const ERROR_MESSAGE_DIV = document.getElementById("error-message-div");

  const DATA = {
    selected: null,
    tasks: [],
  };

  function fetchTasks() {
    return fetch(API_TARGET + "/tasks", {
      headers: {
        Authorization: "Bearer " + getIdentityToken(),
      }
    })
        .then(resp => resp.json(), console.log)
        .then(resp => {
          DATA.tasks = resp.tasks;
        }, console.log);
  }

  function renderTaskList() {
    while (TASKS_LIST.hasChildNodes()) {
      TASKS_LIST.removeChild(TASKS_LIST.firstChild);
    }

    for (let i = 0; i < DATA.tasks.length; i += 1) {
      let task = DATA.tasks[i];
      let a = document.createElement("a");
      a.setAttribute("href", "#!")
      a.classList.add("collection-item");
      if (DATA.selected === task.name) {
        a.classList.add("active");
      }
      a.innerHTML = task.title;
      if (task.done) {
        a.style.setProperty("text-decoration", "line-through");
      }
      a.addEventListener("click", function () {selectTask(task.name)});
      TASKS_LIST.append(a);
    }

    if (!DATA.selected) {
      clearDetails();
    }
  }

  function selectTask(name) {
    let task = getCachedTask(name);
    if (!!task) {
      DATA.selected = name;
      TITLE_INPUT.value = task.title;
      DONE_INPUT.checked = task.done;
      renderTaskList();
    }
  }

  function getCachedTask(name) {
    for (let i = 0; i < DATA.tasks.length; i += 1) {
      let task = DATA.tasks[i];
      if (task.name === name) {
        return task;
      }
    }
  }

  function createTask() {
    DATA.selected = null;
    renderTaskList();
    clearDetails();
    TITLE_INPUT.focus();
  }

  function saveTask() {
    if (!TITLE_INPUT.value) {
      setErrorMessage("Cannot save: Task must have a title.")
      return;
    }

    let task;
    let url;
    if (!!DATA.selected) {
      task = getCachedTask(DATA.selected);
      task.title = TITLE_INPUT.value;
      task.done = DONE_INPUT.checked;
      url = API_TARGET + "/" + task.name;
    } else {
      task = {
        "task": {
          title: TITLE_INPUT.value,
          done: DONE_INPUT.checked,
        }
      }
      url = API_TARGET + "/tasks";
    }

    return fetch(url, {
      method: "POST",
      body: JSON.stringify(task),
      headers: {
        Authorization: "Bearer " + getIdentityToken(),
      }
    })
        .then(resp => resp.json())
        .then(resp => {
          DATA.selected = resp.name;
          setMessage("Task saved.");
        })
        .then(fetchTasks)
        .then(renderTaskList);
  }

  function setMessage(message) {
    MESSAGE_DIV.innerText = message;
    ERROR_MESSAGE_DIV.innerText = "";
  }

  function setErrorMessage(message) {
    MESSAGE_DIV.innerText = "";
    ERROR_MESSAGE_DIV.innerText = message;
  }

  function getIdentityToken() {
    // TODO(hvl): replace with Google SignIn
    let currentUser = CURRENT_USER_INPUT.value;
    if (!currentUser) {
      currentUser = "default-user@example.com";
      CURRENT_USER_INPUT.value = currentUser;
    }
    let payload = {
      email: currentUser,
      iss: "https://fakeaccounts.example.com",
      sub: "foo@example.com",
    }
    return "fakeauth." + btoa(JSON.stringify(payload)) + ".lalala";
  }

  function refresh() {
    fetchTasks()
        .then(renderTaskList);
  }

  function clearDetails() {
    TITLE_INPUT.value = "";
    DONE_INPUT.checked = false;
  }

  CREATE_TASK_BUTTON.addEventListener("click", createTask);
  SAVE_TASK_BUTTON.addEventListener("click", saveTask);

  REFRESH_USER_BUTTON.addEventListener("click", function() {
    DATA.selected = null;
    clearDetails();
    refresh();
  });

  refresh();
})();