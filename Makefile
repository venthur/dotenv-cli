# system python interpreter. used only to create virtual environment
PY = python3
VENV = venv
BIN=$(VENV)/bin

ifeq ($(OS), Windows_NT)
	BIN=$(VENV)/Scripts
	PY=python
endif


.PHONY: all
all: lint mypy test test-release

$(VENV): requirements-dev.txt pyproject.toml
	$(PY) -m venv $(VENV)
	$(BIN)/pip install --upgrade -r requirements-dev.txt
	$(BIN)/pip install -e .['dev']
	touch $(VENV)

.PHONY: test
test: $(VENV)
	# ensure we're using *our* dotenv during testing and not some other one
	# installed on the system
	export PATH=$(BIN):$(PATH)
	$(BIN)/pytest

.PHONY: mypy
mypy: $(VENV)
	$(BIN)/mypy

.PHONY: lint
lint: $(VENV)
	$(BIN)/flake8

.PHONY: build
build: $(VENV)
	rm -rf dist
	$(BIN)/python3 -m build

.PHONY: test-release
test-release: $(VENV) build
	$(BIN)/twine check dist/*

.PHONY: release
release: $(VENV) build
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
