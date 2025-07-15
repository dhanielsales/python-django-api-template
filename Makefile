.PHONY: lint typecheck check

lint:
	ruff check src --fix

typecheck:
	mypy src

check:
	lint typecheck

venv:
	uv venv --python=3.13

install:
	uv sync

makemigrations:
	uv run python src/manage.py makemigrations