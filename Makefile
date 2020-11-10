SHELL := /bin/bash
PWD := $(shell pwd)

all:

build:
	docker build -f ./Dockerfile -t "client:latest" .
.PHONY: build

start: build
	#docker run --rm --network host -v /src:/src client:latest
	docker-compose up --d
.PHONY: start

logs:
	docker-compose logs -f
.PHONY: logs

stop:
	docker-compose stop -t 1
	docker-compose down
.PHONY: stop

debug: build
	docker-compose up --d
	docker-compose logs -f
.PHONY: debug
