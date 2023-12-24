#!/bin/bash

cd src
poetry run alembic revision --autogenerate
poetry run alembic upgrade head
cd ..

git init

poetry run dvc init
poetry run dvc remote add -d minio s3://first
poetry run dvc remote modify minio endpointurl http://$MINIO_HOST:9000
poetry run dvc remote modify minio access_key_id $MINIO_USER
poetry run dvc remote modify minio secret_access_key $MINIO_PASSWORD
poetry run dvc add src/dataframes
poetry run dvc add src/models

poetry run python -m src.api.main
