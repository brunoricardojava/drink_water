# Drink Water

Project developed with the intention of reminding you to drink water.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running](#running)
- [Testing](#testing)

## Prerequisites

- Docker (https://docs.docker.com/engine/install/)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/brunoricardojava/drink_water.git
    cd drink_water
    ```

## Running

1. Start the application container

    ```bash
    docker compose up
    ```

The application will be available at [http://0.0.0.0:5001/](http://0.0.0.0:5001/).

ENDPOINTS:

[POST] /api/v1/user

[PUT] /api/v1/user/<user_id>

[POST] /api/v1/user/<user_id>/action

[GET] /api/v1/user/<user_id>/action

[GET] /api/v1/user/<user_id>/goal

## Testing

1. To run the tests, use:

    ```bash
    docker compose exec web poetry run task test
    ```

2. To check the test coverage, use:

    ```bash
    docker compose exec web poetry run task coverage
    ```

You can access the test coverage report at project-path/htmlcov/index.html
