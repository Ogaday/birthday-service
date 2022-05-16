# Birthday Service

A simple application to store and serve birthdays.

Consists of a [FastAPI](https://fastapi.tiangolo.com/) app with a SQL backend.

## Docs

Consists of two endpoints:

1. Save/Update the given user's name and date of birth

```
Request: PUT /hello/<username> {"dateOfBirth": "YYY-MM-DD"}
Response: 204 No Content
```

2. Return a hello birthday message for the given user

```
Request: GET /hello/<username>
Response: 200 OK
```

OpenAPI docs are additionally served at `/docs`.

## Development

App can be installed and run locally:

```
pip install ".[dev]"
./scripts/serve.sh
```

linting and tests can be run as follows:

```
./scripts/lint.sh
./scripts/test.sh
```

Arguments to `test.sh` and `serve.sh` are passed through to `pytest` and `uvicorn`
respectively.

### Docker

And via Docker. Build and run tests:

```
docker build --target=dev -t birthday-service-dev .
docker run birthday-service-dev -- ./scripts/test.sh
```

Serve locally on port `5000` with a postgres backend:

```
docker build -t birthday-service .
docker run --rm --env-file example.env -d -p 5432:5432 postgres
docker run --rm --env-file example.env -it --net host birthday-service ./scripts/serve.sh --host 0.0.0.0 --port 5000
```
