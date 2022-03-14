FROM python:3.10.1-slim

WORKDIR /app

ENV PYTHONPATH=${PYTHONPATH}:${PWD}

RUN python -m pip install --upgrade pip && pip install poetry
RUN poetry config virtualenvs.create false

COPY pyproject.toml .
RUN poetry install

CMD python kafka_to_clickhouse/main.py
