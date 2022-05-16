#!/usr/bin/env bash
set -e
set -x

uvicorn birthday_service.app:app $@
