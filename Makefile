.DEFAULT_GOAL := help
TARGET = origin/master
SRC = src/*

define find.functions
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done
endef

help: # Show help for each of the Makefile recipes.
	@echo 'The following commands can be used.'
	@echo ''
	$(call find.functions)

leave: clean # Cleanup and deactivate venv
	deactivate

clean: # Clean needless files
	rm -rf __pycache__ .mypy_cache .ruff_cache

lint: # Static files check
	ruff check --exit-zero $(SRC)
	darker --revision $(TARGET) --diff --check $(SRC)

lint-path: # Static files check by path
	ruff check --exit-zero $(path)
	darker --revision $(TARGET) --diff --check $(path)

format: # Format files
	ruff --fix --silent --exit-zero $(SRC)
	darker --revision $(TARGET) $(SRC)

format-path: # Format files by path
	ruff --fix --silent --exit-zero $(path)
	darker --revision $(TARGET) $(path)

typecheck: # Type check
	mypy src/*.py

typecheck-path: # Type check by path
	mypy $(path)

security-check: # Security check
	bandit $(SRC)

run-app: # Run api app
	poetry run python -m src.api.main

run-tests: # Run tests
	poetry run pytest tests

.PHONY: help clean leave lint lint-path format format-path typecheck typecheck-path security-check run-app run-tests