install:
	pip install -e .

install-ct2:
	pip install -e ".[ct2]"

lint:
	ruff check .

type:
	mypy packages

test:
	pytest

tasks:
	scripts/list-tasks.sh

tasks-pending:
	scripts/list-pending-tasks.sh

tasks-done:
	scripts/summarize-completed-tasks.sh

tasks-snapshot:
	scripts/snapshot-backlog.sh
