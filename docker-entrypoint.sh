#!/bin/bash

poetry run alembic revision --autogenerate
poetry run alembic upgrade head

git init
poetry run dvc init
poetry run dvc remote add -d minio s3://first
poetry run dvc remote modify minio endpointurl http://minio:9000
poetry run dvc remote modify minio access_key_id minio
poetry run dvc remote modify minio secret_access_key minio123
poetry run dvc add dataframes
poetry run dvc add models

poetry run python -m api.main
