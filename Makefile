#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_NAME = cleanflow-ml
PYTHON_VERSION = 3.13
VENV_DIR = .venv
PYTHON_INTERPRETER = $(VENV_DIR)/Scripts/python   # Windows padrão
ifeq ($(OS),Linux)
    PYTHON_INTERPRETER = $(VENV_DIR)/bin/python  # Linux/macOS
endif

#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Install Python dependencies (production)
.PHONY: requirements
requirements:
	$(PYTHON_INTERPRETER) -m pip install -U pip
	$(PYTHON_INTERPRETER) -m pip install -e .

## Install Python dependencies (development)
.PHONY: dev
dev:
	$(PYTHON_INTERPRETER) -m pip install -e ".[dev]"

## Delete all compiled Python files and caches
.PHONY: clean
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

## Lint using ruff (check only)
.PHONY: lint
lint:
	ruff check src tests

## Format source code with black + ruff
.PHONY: format
format:
	black src tests
	ruff check --fix src tests

## Create virtual environment
.PHONY: create_environment
create_environment:
	@python -m venv $(VENV_DIR)
	@echo ">>> Virtualenv created at $(VENV_DIR). Activate with:\nsource $(VENV_DIR)/bin/activate (Linux/macOS)\n$(VENV_DIR)\Scripts\activate.bat (Windows)"

#################################################################################
# PROJECT RULES                                                                 #
#################################################################################

## Load dataset
.PHONY: data
data: requirements
	$(PYTHON_INTERPRETER) src/application/usecases/load_raw_data_usecase.py

## Run tests
.PHONY: test
test: dev
	$(PYTHON_INTERPRETER) -m pytest -v

#################################################################################
# COMBINED SETUP                                                                #
#################################################################################

## Full project setup (venv + dev dependencies)
.PHONY: setup
setup: create_environment dev lint format test
	@echo ">>> Project setup complete."

#################################################################################
# SELF-DOCUMENTING COMMANDS                                                     #
#################################################################################

.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys; \
lines = '\n'.join([line for line in sys.stdin]); \
matches = re.findall(r'\n## (.*)\n[\s\S]+?\n([a-zA-Z_-]+):', lines); \
print('Available rules:\n'); \
print('\n'.join(['{:25}{}'.format(*reversed(match)) for match in matches]))
endef
export PRINT_HELP_PYSCRIPT

help:
	@$(PYTHON_INTERPRETER) -c "${PRINT_HELP_PYSCRIPT}" < $(MAKEFILE_LIST)