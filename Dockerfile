FROM python:3.9

RUN pip3 install "poetry==1.7.0"

COPY poetry.lock pyproject.toml ./
RUN poetry install

COPY src ./mlops/src

WORKDIR mlops/

RUN mkdir src/models src/dataframes

COPY docker-entrypoint.sh ./
RUN chmod +x docker-entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["./docker-entrypoint.sh"]
