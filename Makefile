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

migrate:
	uv run python src/manage.py migrate

test:
	uv run pytest

runcelery:
	cd src && uv run celery -A config worker --loglevel=info

runserver:
	uv run python src/manage.py runserver