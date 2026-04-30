#!/bin/bash

poetry run alembic upgrade head

poetry run uvicorn --host 0.0.0.0  --port 3000 src.app:app