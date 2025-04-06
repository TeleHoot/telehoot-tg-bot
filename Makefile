# Makefile for Telegram Bot project

.DEFAULT_GOAL:=help
.ONESHELL:
.EXPORT_ALL_VARIABLES:
MAKEFLAGS += --no-print-directory

# Variables
DOCKER_COMPOSE = docker-compose
DOCKER_COMPOSE_PROD = docker-compose -f docker-compose.prod.yml
UV = uv
PRE_COMMIT = pre-commit
PYTEST = pytest
RUFF = ruff
PYRIGHT = pyright

# Help command
help:
	@echo "Available commands:"
	@echo ""
	@echo "== Development Environment =="
	@echo "  up           - Start development containers (Docker)"
	@echo "  down         - Stop and remove development containers"
	@echo "  dev          - Start bot in development mode with reload"
	@echo ""
	@echo "== Production Environment =="
	@echo "  prod         - Deploy production containers"
	@echo "  down-prod    - Stop and remove production containers"
	@echo ""
	@echo "== Dependency Management =="
	@echo "  install-deps - Install all dependencies with dev extras"
	@echo ""
	@echo "== Code Quality & Testing =="
	@echo "  check        - Run all pre-commit checks"
	@echo "  lint         - Check code style with Ruff (with auto-fix)"
	@echo "  format       - Format code with Ruff formatter"
	@echo "  type-check   - Static type checking with Pyright"
	@echo "  test         - Run tests with pytest"
	@echo ""
	@echo "== Application Control =="
	@echo "  start        - Run bot in production mode"
	@echo "  debug        - Run bot in debug mode"
	@echo ""
	@echo "== Project Setup =="
	@echo "  uinit              - Unix setup: install deps + create .env"
	@echo "  winit              - Windows setup: install deps + create .env"
	@echo "  create-env-unix    - Create .env from example (Unix)"
	@echo "  create-env-windows - Create .env from example (Windows)"
	@echo ""
	@echo "== Miscellaneous =="
	@echo "  help         - Show this help message"

# Docker commands
up:
	$(DOCKER_COMPOSE) up -d --build

down:
	$(DOCKER_COMPOSE) down

prod:
	$(DOCKER_COMPOSE_PROD) up -d --build

down-prod:
	$(DOCKER_COMPOSE_PROD) down

# Dependency management
install-deps:
	$(UV) sync --all-extras --dev

# Code quality
check:
	$(UV) run $(PRE_COMMIT) run --all-files

lint:
	$(UV) run $(RUFF) check --fix .

format:
	$(UV) run $(RUFF) format .

type-check:
	$(UV) run $(PYRIGHT)

# Testing
test:
	$(UV) run $(PYTEST) -v --durations=0 tests/

# Application control
start:
	$(UV) run python -m bot

debug:
	$(UV) run python -m bot --debug

# Create .env file from example.env on Unix systems
create-env-unix:
	@if [ -f .env ]; then \
		echo ".env file already exists. Aborting to avoid overwriting."; \
	else \
		cp example.env .env; \
		echo ".env file created from example.env."; \
	fi

# Create .env file from example.env on Windows systems
create-env-windows:
	@if exist .env ( \
		echo .env file already exists. Aborting to avoid overwriting. \
	) else ( \
		copy example.env .env && \
		echo .env file created from example.env. \
	)

# Initialize the project on Unix systems (install dependencies, create .env file)
uinit: install-deps create-env-unix
	@echo "Project initialized for Unix systems."

# Initialize the project on Windows systems (install dependencies, create .env file)
winit: install-deps create-env-windows
	@echo "Project initialized for Windows systems."

# Start the development environment and the app
dev: up migrate start

.PHONY: help up down prod down-prod install-deps check lint format type-check test start debug create-env-unix create-env-windows uinit winit dev
