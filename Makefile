# system python interpreter. used only to create virtual environment
PY = python3
VENV = venv
BIN=$(VENV)/bin

ifeq ($(OS), Windows_NT)
	BIN=$(VENV)/Scripts
	PY=python
endif


.PHONY: all
all: test lint mypy

$(VENV): requirements-dev.txt pyproject.toml
	$(PY) -m venv $(VENV)
	$(BIN)/python -m pip install --upgrade pip
	$(BIN)/pip install --upgrade -r requirements-dev.txt
	$(BIN)/pip install -e .
	touch $(VENV)

.PHONY: test
test: $(VENV)
	$(BIN)/pytest

.PHONY: mypy
mypy: $(VENV)
	$(BIN)/mypy

.PHONY: lint
lint: $(VENV)
	$(BIN)/flake8

.PHONY: release
release: $(VENV)
	rm -rf dist
	$(BIN)/python -m build
	$(BIN)/twine upload dist/*

VERSION = $(shell python3 -c 'from dotenv_cli import __VERSION__; print(__VERSION__)')
tarball:
	git archive --output=../dotenv-cli_$(VERSION).orig.tar.gz HEAD

.PHONY: clean
clean:
	rm -rf build dist *.egg-info
	rm -rf $(VENV)
	find . -type f -name *.pyc -delete
	find . -type d -name __pycache__ -delete
	# coverage
	rm -rf htmlcov .coverage
	rm -rf .mypy_cache
	rm -rf .pytest_cache
