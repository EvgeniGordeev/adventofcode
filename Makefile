#!make
.PHONY: docker-build

ifndef VERBOSE
MAKEFLAGS += --no-print-directory
endif

# multi-platform docker build and push to
build-ci:
	bin/build-ci-image.sh

pip-req:
	echo "# Built from Pipfile with 'pipenv requirements'" > requirements.txt
	pipenv requirements >> requirements.txt