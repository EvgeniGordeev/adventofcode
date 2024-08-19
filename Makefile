#!make
.PHONY: docker-build

ifndef VERBOSE
MAKEFLAGS += --no-print-directory
endif

build-ci:
	bin/build-ci-image.sh