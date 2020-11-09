SHELL := /bin/bash
PWD := $(shell pwd)

all:

build:
	docker build -f ./Dockerfile -t "client:latest" .
.PHONY: build

start: build
	docker run --rm --network host client:latest
.PHONY: start
