.PHONY: clean install test

DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
SHELL=/bin/bash

ENV := $(DIR)/env/bin
PYTHON := $(ENV)/python
PIP := $(ENV)/pip
FAB := $(ENV)/fab
PELICAN := $(ENV)/pelican

STATUS_ERROR := \033[1;31m*\033[0m Error
STATUS_OK := \033[1;32m*\033[0m OK


clean-pyc:
	find . -name '*.pyc' -exec rm -f {} + ;\
	find . -name '*.pyo' -exec rm -f {} + ;\
	find . -name '*~' -exec rm -f {} + ;\
	if [ $$? -eq 0 ]; then \
		echo -e "${STATUS_OK}" ;\
	else \
		echo -e "${STATUS_ERROR}" ;\
	fi;

clean: clean-pyc


install-env-python2:
	rm -rf "$(DIR)/env/" ;\
	virtualenv -p /usr/bin/python2 --clear "$(DIR)/env/" ;\
	if [ $$? -eq 0 ]; then \
		echo -e "${STATUS_OK}" ;\
	else \
		echo -e "${STATUS_ERROR}" ;\
	fi;

install-env-python3:
	rm -rf "$(DIR)/env/" ;\
	virtualenv -p /usr/bin/python3 --clear "$(DIR)/env/" ;\
	if [ $$? -eq 0 ]; then \
		echo -e "${STATUS_OK}" ;\
	else \
		echo -e "${STATUS_ERROR}" ;\
	fi;

env-activate:
	. $(ENV)/activate

install-python-libs:
	$(PIP) install -U pip ;\
	$(PIP) install --no-cache-dir --upgrade -r "$(DIR)/requirements.txt" ;\
	if [ $$? -eq 0 ]; then \
		echo -e "${STATUS_OK}" ;\
	else \
		echo -e "${STATUS_ERROR}" ;\
	fi;

install: install-env-python3 env-activate install-python-libs


test:
	$(DIR)/env/bin/py.test \
	-v \
	-q --flakes \
	--cov-config=.coveragerc \
	--cov=hubstaff \
	--cov-report=html \
	--doctest-modules \
	tests
