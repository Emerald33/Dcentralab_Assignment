VENV_PATH := $(shell poetry env info --path)

POETRY_INSTALLED := $(shell command -v poetry > /dev/null && echo "yes" || echo "no")

# Rule to install Poetry and dependencies if Poetry is not found
install_poetry:
	if [ "$(POETRY_INSTALLED)" = "no" ]; then \
		echo "Poetry is not installed. Installing Poetry..."; \
		pip install poetry; \
		echo "Poetry installed. Installing project dependencies..."; \
		poetry install --no-root; \
	else \
		echo "Poetry is already installed."; \
	fi

# Rule to activate the virtual environment
env:
	@echo "Activating the virtual environment..."
	@bash -c "source $(VENV_PATH)/bin/activate && echo 'Virtual environment activated'"

# Run setup commands for crawl4ai
setup:
	poetry run crawl4ai-setup
	poetry run crawl4ai-doctor

# Main rule to install Poetry, install dependencies, activate environment, and setup
all: install_poetry env setup
