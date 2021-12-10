test:
	poetry run pytest --junit-xml=./tests/coverage.xml
coverage:
	poetry run coverage run -m pytest
build:
	poetry build
install:
	poetry install
lint:
	poetry run flake8
check:
	poetry check
.PHONY: install test lint check build paginator