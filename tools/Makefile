PROJECT_NAME=pyfolio
TEST_DIR=tests

PYTHON=python3
DOCKER_IMAGE=${PROJECT_NAME}-docker
DOCKER_RUN=docker run \
 -u $(shell id -u):$(shell id -g) \
 -v $(shell pwd)/$(PROJECT_NAME):/work/$(PROJECT_NAME) \
 -v $(shell pwd)/$(TEST_DIR):/work/$(TEST_DIR)

TWINE_USERNAME=__token__

LINE_LENGTH=100

.PHONY: build doc dist

all: format lint

help: ## Print help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

clean: ## Remove all the generated files
	@rm -rf *.dist-info *.egg-info
	@rm -rf dist build
	@rm -rf ${PROJECT_NAME}/__pycache__ ${PROJECT_NAME}/*.pyc ${PROJECT_NAME}/*.pyo

format: ## Run isort and black to format Python code
	@${PYTHON} -m isort --line-length ${LINE_LENGTH} --profile black . ${PROJECT_NAME} ${TEST_DIR}
	@${PYTHON} -m black --line-length ${LINE_LENGTH} *.py ${PROJECT_NAME}/**.py ${TEST_DIR}/**.py

lint: ## Check Python code with isort, black and pylint to identify any problem
	${PYTHON} -m isort --line-length ${LINE_LENGTH} --profile black --check . ${PROJECT_NAME} ${TEST_DIR}
	${PYTHON} -m black --line-length ${LINE_LENGTH} --check *.py ${PROJECT_NAME}/**.py ${TEST_DIR}/**.py
	${PYTHON} -m pylint --ignore-patterns='.*\.yml' ${PROJECT_NAME} ${TEST_DIR}

test: ## Run python tests with pytest
	pytest


dist: ## Build wheel for the package
ifndef VERSION
	$(error VERSION variable missing. It defines the package version name.)
endif
	@echo Creating wheel for $(PROJECT_NAME):$(VERSION)
	$(PYTHON) setup.py bdist_wheel --universal

upload_dist: ## Upload package to pypi
ifndef TWINE_PASSWORD
	$(error TWINE_PASSWORD must be defined)
endif
	$(PYTHON) -m twine upload dist/* \
		-u $(TWINE_USERNAME) \
		-p $(TWINE_PASSWORD)

build: ## Build docker image
	docker build -t $(DOCKER_IMAGE) .

docker_%: ## Run `make %` inside docker container
docker_%: build
	@echo running `make $(shell echo $@ | cut -d_ -f2-)` in docker container
	@$(DOCKER_RUN) $(OPTIONS) \
		-t $(DOCKER_IMAGE) \
		$(shell echo $@ | cut -d_ -f2-)

docker_dist: ## Run `make dist` with docker
docker_dist: build
	mkdir -p dist
	@$(DOCKER_RUN) $(OPTIONS) \
		-v $(shell pwd)/dist:/work/dist \
		-e VERSION \
		-t $(DOCKER_IMAGE) \
		dist

docker_upload_dist: ## Run `make upload_dist` with docker
docker_upload_dist: build
	mkdir -p dist
	@$(DOCKER_RUN) $(OPTIONS) \
		-v $(shell pwd)/dist:/work/dist \
		-e TWINE_PASSWORD \
		-t $(DOCKER_IMAGE) \
		upload_dist

_interactive: ## Enter the docker container in interactive mode
_interactive: build
	$(DOCKER_RUN) --entrypoint /bin/bash -i $(OPTIONS) -t $(DOCKER_IMAGE)


check_me.yml: ## Check ../me.yml file using pyfolio
check_me.yml: build
	$(DOCKER_RUN) \
		-v  $(shell pwd)/../me.yml:/work/me.yml \
		--entrypoint /work/venv/bin/python3 \
		$(OPTIONS) -t $(DOCKER_IMAGE) \
		-m $(PROJECT_NAME) check me.yml --fail-at ERROR

translate_%: ## Translate jekyll source using overrides in `jekyll-%` folder using docker
translate_%: build
	@echo Translating jekyll in '$(shell echo $@ | cut -d_ -f2-)'
	mkdir -p "$(shell pwd)/../$(shell echo $@ | cut -d_ -f2-)-tmp/"
	$(DOCKER_RUN) \
		-v  $(shell pwd)/../jekyll-$(shell echo $@ | cut -d_ -f2-)/:/work/override/ \
		-v  $(shell pwd)/../$(shell echo $@ | cut -d_ -f2-)-tmp/:/work/dest/ \
		-v  $(shell pwd)/../jekyll/:/work/source/ \
		--entrypoint /work/venv/bin/python3 \
		$(OPTIONS) -t $(DOCKER_IMAGE) \
		-m $(PROJECT_NAME) translate /work/source/ /work/dest/ /work/override/ --force
