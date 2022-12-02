FROM python:3.10-buster as builder

ENV POETRY_VERSION=1.2.2 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_HOME=/opt/poetry
RUN curl -sSL https://install.python-poetry.org | python
ENV PATH /opt/poetry/bin:$PATH

WORKDIR /app
COPY . /app/
RUN poetry install --no-interaction --no-ansi

EXPOSE 4938/tcp
ENTRYPOINT ["poetry", "run", "gunicorn", "--bind", "0.0.0.0:4938", "octopus-proxy.app"]
