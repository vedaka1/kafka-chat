FROM python:3.12.4-slim-bullseye

WORKDIR /app

ENV PYTHONPATH=.

RUN pip install --upgrade pip
RUN pip install poetry==1.7.1

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false
RUN poetry install --without test --no-root --no-interaction --no-ansi

COPY app/ ./

EXPOSE 8000

CMD [ "python", "main.py" ]