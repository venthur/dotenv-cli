# system python interpreter. used only to create virtual environment
PY = python3
VENV = venv
BIN=$(VENV)/bin

DOCS_SRC = docs
DOCS_OUT = site

ifeq ($(OS), Windows_NT)
	BIN=$(VENV)/Scripts
	PY=python
endif


.PHONY: all
all: lint mypy test test-docs test-release

$(VENV): requirements-dev.txt pyproject.toml
	$(PY) -m venv $(VENV)
	$(BIN)/pip install --upgrade -r requirements-dev.txt
	$(BIN)/pip install -e .['dev']
	touch $(VENV)

# in this target, our tests are using Popen etc to run other scrips. Therefore
# we must set the PATH to include the virtual environment's bin directory
.PHONY: test
test: PATH := $(BIN):$(PATH)
test: $(VENV)
	$(BIN)/pytest

.PHONY: mypy
mypy: $(VENV)
	$(BIN)/mypy

.PHONY: lint
lint: $(VENV)
	$(BIN)/ruff check .

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

.PHONY: test-docs
test-docs: $(VENV)
	# we try to keep the README and the docs/index.md in sync
	@cmp README.md docs/index.md

.PHONY: docs
docs: $(VENV)
	$(BIN)/mkdocs build

VERSION = $(shell python3 -c 'from dotenv_cli import __VERSION__; print(__VERSION__)')
tarball:
	git archive --output=../dotenv-cli_$(VERSION).orig.tar.gz HEAD

.PHONY: clean
clean:
	rm -rf build dist *.egg-info
	rm -rf $(VENV)
	rm -rf $(DOCS_OUT)
	find . -type f -name *.pyc -delete
	find . -type d -name __pycache__ -delete
	# coverage
	rm -rf htmlcov .coverage
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	rm -rf .ruff_cache
