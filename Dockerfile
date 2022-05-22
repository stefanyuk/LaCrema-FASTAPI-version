# ===================== Builder =========================
FROM python:3.10-alpine3.13 AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=false \
    POETRY_NO_INTERACTION=1 \
    POETRY_HOME=/opt/poetry \
    POETRY_CACHE_DIR="/opt/poetry/cache"

WORKDIR /app

RUN apk update \
    && apk add libffi-dev build-base curl \
    && curl -sSL https://install.python-poetry.org | python3 - \
    # Simulate the restaurantservice package, so poetry can install all the dependencies.
    && mkdir /app/restaurantservice \
    && touch /app/restaurantservice/__init__.py

COPY pyproject.toml poetry.lock /app/
RUN ${POETRY_HOME}/bin/poetry install --no-dev

# ===================== Production =========================
FROM python:3.10-alpine3.13 as production

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=false \
    POETRY_NO_INTERACTION=1 \
    POETRY_HOME=/opt/poetry \
    POETRY_CACHE_DIR="/opt/poetry/cache"

WORKDIR /app

RUN apk add curl

COPY --from=builder $POETRY_HOME $POETRY_HOME
COPY ./ /app

EXPOSE 80

CMD [ "/opt/poetry/bin/poetry", "run", "uvicorn", "restaurantservice.app:app", "--host", "0.0.0.0", "--port", "80" ]
