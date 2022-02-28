# Task Master

The project is made of two parts: a frontend server and an API server.

Each server can be started from the command line with a Make recipe called `run`
. By default, the frontend will run on port 8080 and the API on port 8081.

For the Python backend a Virtual Environment should be created first. This can
be done with the Make recipe `venv`.

## Dependencies

Running the services requires the following dependencies.

* Python 3.8 (or higher)
* Virtualenv
* Go 17 (or higher)
* GNU Make

## Running a Test

As requested, a single (unit) test has been implemented for the API. This test
can be run via the `test` recipe.

## Files & Structure

```
.
|-- README.md                   This readme file
|-- backend
|   |-- Makefile                GNU Make recipes for running server 
|   |-- Procfile                for building with buildpacks.io (unused/todo)
|   |-- main.py                 main server code
|   |-- models.py               models used in various places
|   |-- persistence.py          data persistence interface and implementations
|   |-- requirements.txt
|   `-- test_main.py            unit test with a somewhat convoluted test
`-- frontend
    |-- Makefile                GNU Make recipes for running server
    |-- files                   website statics
    |   |-- index.html
    |   `-- static
    |       `-- js
    |           `-- main.js
    |-- go.mod
    `-- server.go               minimal frontend server code
```
