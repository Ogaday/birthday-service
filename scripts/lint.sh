#!/usr/bin/env bash
set -e
set -x

flake8 birthday_service tests
isort --diff birthday_service tests
mypy birthday_service tests
black --diff birthday_service tests
