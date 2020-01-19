SHELL := /bin/bash

env:
	python3 -m venv env --system-site-packages;

dep:
	source ./env/bin/activate; \
	python3 -m pip install --upgrade pip; \
	python3 -m pip install .; \

user:
	source ./env/bin/activate; \
	cd itemet; \
	python3 -m flask fab create-admin;

remove:
	rm -Rf ./env;
	rm -Rf ./demo/flask.db;
	rm -Rf ./demo/select;

install: remove env dep user

run:
	source ./env/bin/activate; \
	cd itemet; \
	python3 run.py;
