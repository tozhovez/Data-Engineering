AWS_PROFILE_DEV := default

PROJECTNAME=$(shell basename "$(PWD)")
PACKAGE_PREFIX := data-analytics
PACKAGE := data-analytics
PYTHON := $(shell which python)
PIP := $(shell which pip)
PYV := $(shell $(PYTHON) -c "import sys;t='{v[0]}.{v[1]}'.format(v=list(sys.version_info[:2]));sys.stdout.write(t)")
PWD := $(shell pwd)
SHELL = /bin/bash
EXPORT_VERSION = $(eval VERSION=$(shell cat .version))
REQ_FILE = ./Infra/requirements.txt
#   Makefile

.PHONY: clean

.DEFAULT_GOAL: help

help: ## Show this help
	@printf "\n\033[33m%s:\033[1m\n" 'Choose available commands run in "$(PROJECTNAME)"'
	@echo "======================================================"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[32m%-14s		\033[35;1m-- %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@printf "\033[33m%s\033[1m\n"
	@echo "======================================================"

envs: ## Print environment variables
	@echo "======================================================"
	@echo  "REQ_FILE: $(REQ_FILE)"
	@echo  "PYTHON: $(PYTHON)"
	@echo  "PIP: $(PIP)"
	@echo  "PYV: $(PYV)"
	@echo  "shell $(SHELL)"
	@echo  "pwd $(PWD)"
	@echo "======================================================"

initial: clean update install-requirements install-serverless ## Install tools and start dev env


update: ## Do apt upgrade and autoremove
	@echo "======================================================"
	sudo apt update && sudo apt upgrade -y
	sudo apt autoremove -y

install-requirements: ## Install requirements
	@echo "======================================================"
	$(PYTHON) -m pip install --upgrade pip
	$(PIP) install --upgrade pip
	$(PYTHON) -m pip install -r $(REQ_FILE) --upgrade
	$(PIP) install -r $(REQ_FILE) --upgrade
	@echo "======================================================"

set-aws-dev-profile: ## SET AWS DEV PROFILE
	@export AWS_PROFILE=$(AWS_PROFILE_DEV)


install-serverless: ## Install serverless via npm (npm must be installed)
	@echo "======================================================"
	@echo "Install serverless via npm (npm must be installed)"
	@echo "======================================================"
	@npm install -g serverless


deploy-etl-process: ## Deploying etl-process lambdas to aws cloud
	@echo "======================================================"
	@echo "deploying etl-process lambdas to aws cloud"
	@echo "======================================================"
	@cd data_analytics_serverless && npm install
	@cd data_analytics_serverless && SLS_DEBUG=1 serverless deploy --config serverless.yml --stage dev-etl --aws-profile $(AWS_PROFILE_DEV) --verbose


invoke-etl-process: ## invoke etl-processes lambdas in aws cloud
	@echo "======================================================"
	@echo "invoke etl-processes lambdas in aws cloud"
	@echo "======================================================"
	@cd data_analytics_serverless && npm install
	@cd data_analytics_serverless && serverless logs --config serverless.yml -f -t --stage dev-etl --aws-profile $(AWS_PROFILE_DEV) --verbose &


remove-etl-process: ## Remove etl-process
	@echo "======================================================"
	@cd data_analytics_serverless && serverless && remove --config serverless.yml --stage dev-etl --aws-profile $(AWS_PROFILE_DEV) --verbose

clean: ## Clean sources
	@echo "======================================================"
	@echo clean $(PROJECTNAME)
	@echo $(find ./* -maxdepth 0 -name "*.pyc" -type f)
	echo $(find . -name ".DS_Store" -type f)
	@rm -fR __pycache__ venv "*.pyc"
	@find ./* -maxdepth 0 -name "*.pyc" -type f -delete
	@find ./* -name '*.py[cod]' -delete
	@find ./* -name '__pycache__' -delete
	find . -name '*.DS_Store' -delete


list: ## Makefile target list
	@echo "======================================================"
	@echo Makefile target list
	@echo "======================================================"
	@cat Makefile | grep "^[a-z]" | awk '{print $$1}' | sed "s/://g" | sort
