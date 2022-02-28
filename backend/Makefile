VENV := . .venv/bin/activate

REGION := europe-west1

NAME := taskmaster-api
LOCAL_PORT := 8081


check-project:
ifndef PROJECT
	$(error Missing PROJECT)
endif


venv:
	virtualenv -p python3 .venv
	$(VENV) && pip install -r requirements.txt

test:
	$(VENV) && pytest

run:
	export PORT=$(LOCAL_PORT) && \
	$(VENV) && python main.py

run-gunicorn:
	export PORT=$(LOCAL_PORT) && \
	$(VENV) && gunicorn \
		--workers 1 \
		--threads 8 \
		--timeout 10 \
		--capture-output \
		--enable-stdio-inheritance \
		'main:main()'


smoke-test-list:
	curl \
		-H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6ImFjYjZiZTUxZWZlYTZhNDE5ZWM5MzI1ZmVhYTFlYzQ2NjBmNWIzN2MiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiIzMjU1NTk0MDU1OS5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsImF1ZCI6IjMyNTU1OTQwNTU5LmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwic3ViIjoiMTAwOTY0NDY3OTczMzYzMDgzNzU3IiwiaGQiOiJpbmNlbnRyby5jb20iLCJlbWFpbCI6ImhheW8udmFubG9vbkBpbmNlbnRyby5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiYXRfaGFzaCI6ImZ5NGhBQ1ZHNTZCYlRTQlV3Z1Z4MXciLCJpYXQiOjE2NDYwMzc5NTcsImV4cCI6MTY0NjA0MTU1N30.Yz54Ua3e3CY3BEgD-N-JAURwXDcK6TlCLlYPVv5E9oErDh8EeGvKMu8YLF-0UL3nTVjSlj7J6GZ768qQQIAkX3TBO0LIGlhrecprCwi8TDr__20Dw7xYWF9zjdYpX3OWK82Abfu3EspPfGeg9JX-yhTUhR7cIZcP9iZ06nxv02h_BenbZgRR4TOeiehnsiSfQZ8sUAC-pnoqA0r6acOUM5mrwMDcLjdYI9YZFV9VlXDSdI-id9tC4knNQQq-S_qVtbg7z_j7FR5klSzfUJu07QivA25-NI2c5Swg1J41OlG_AypyYGRoVZBeNe32ipDHgkedOdNjCTdOsfkQpIx_lg" \
		http://localhost:$(LOCAL_PORT)/tasks

smoke-test-create:
	curl \
		-H "Content-Type: application/json" \
		-d '{"task": {"title": "smoke test title '$$(date +%s)'"}}' \
		http://localhost:$(LOCAL_PORT)/tasks

smoke-test-update:
ifndef ID
	$(error missing task ID)
endif
	curl \
		-H "Content-Type: application/json" \
		-d '{"title": "some smoke test update"}' \
		http://localhost:$(LOCAL_PORT)/tasks/$(ID)
