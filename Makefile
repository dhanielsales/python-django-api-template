.PHONY: lint typecheck check

lint:
	ruff check src --fix

typecheck:
	mypy src

check: lint typecheck