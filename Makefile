install:
	pip install -e .

lint:
	ruff check .

type:
	mypy packages

test:
	pytest
