ARG PYTHON_VERSION=3.11

FROM python:${PYTHON_VERSION}-alpine

WORKDIR /app

# ---POETRY SETUP---
ENV POETRY_VERSION=1.7.1
# Remove a interação do usuario
ENV POETRY_NO_INTERACTION=true
# Não cria ambientes virtuais na intalação das dependencias do projeto pelo poetry
ENV POETRY_VIRTUALENVS_CREATE=false
# Pasta de ambiente virtual não é setado no projeto
ENV POETRY_VIRTUALENVS_IN_PROJECT=false
# Diretorio de cache do poetry
ENV POETRY_CACHE_DIR=/tmp/poetry_cache

RUN pip install poetry==${POETRY_VERSION}

COPY . .

RUN poetry install --without dev --no-root && rm -rf ${POETRY_CACHE_DIR}
