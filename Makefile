VERSION = $(shell python3 setup.py --version)

all: lint test

test:
	pytest
.PHONY: test

lint:
	flake8
.PHONY: lint

docs:
	$(MAKE) -C docs html
.PHONY: docs

release:
	python3 setup.py sdist bdist_wheel
	twine upload dist/*
.PHONY: release

tarball:
	git archive --output=../dotenv-cli_$(VERSION).orig.tar.gz HEAD

clean:
	find . -type f -name *.pyc -delete
	find . -type d -name __pycache__ -delete
.PHONY: clean
