# Drink Water

Projeto desenvolvimedo com o intuito de lembrar de beber agua.

## Sumário

- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Execução](#execução)
- [Testes](#testes)

## Pré-requisitos

- Docker

## Instalação

1. Clone o repositório:

    ```bash
    git clone https://github.com/brunoricardojava/drink_water.git
    cd drink_water
    ```

## Execução

1. Suba o container da aplicação

    ```bash
    docker compose up
    ```

A aplicação estará disponível em [http://0.0.0.0:5001/](http://0.0.0.0:5001/).

## Testes

1. Para rodar os testes, use:

    ```bash
    docker compose exec web poetry run task test
    ```

2. Para verificar a cobertura de testes, use:

    ```bash
    docker compose exec web poetry run task coverage
    ```

Podera acessar o relatorio de cobertura dos testes em project-path/htmlcov/index.html
