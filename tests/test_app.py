from os.path import join
from tempfile import TemporaryDirectory

import pytest
from fastapi.testclient import TestClient
from freezegun import freeze_time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from birthday_service.app import app, get_db
from birthday_service.models import Base


@pytest.fixture
def dummy_engine():
    with TemporaryDirectory() as tmpdir:
        path = join(tmpdir, "birthday.db")
        engine = create_engine(f"sqlite:///{path}", echo=True)
        Base.metadata.create_all(bind=engine)
        yield engine


@pytest.fixture
def client(dummy_engine):
    DummySessionLocal = sessionmaker(bind=dummy_engine)

    def override_get_db():
        db = DummySessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


@freeze_time("2022-05-15 12:00")
def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"utcnow": "2022-05-15T12:00:00"}


def test_no_user(client):
    response = client.get("/hello/nobody")
    assert response.status_code == 404


@freeze_time("2022-05-15 12:00")
def test_round_trip(client):
    payload = {"dateOfBirth": "2020-06-01"}
    put_response = client.put("/hello/guido", json=payload)
    assert put_response.status_code == 204
    get_response = client.get("/hello/guido")
    assert get_response.status_code == 200
    assert get_response.json() == {
        "message": "Hello, guido! Your birthday is in 17 days"
    }


@freeze_time("2022-05-15 12:00")
def test_round_trip_next_day(client):
    payload = {"dateOfBirth": "2020-05-16"}
    put_response = client.put("/hello/guido", json=payload)
    assert put_response.status_code == 204
    get_response = client.get("/hello/guido")
    assert get_response.status_code == 200
    assert get_response.json() == {"message": "Hello, guido! Your birthday is in 1 day"}


@freeze_time("2022-05-15 12:00")
def test_round_trip_same_day(client):
    payload = {"dateOfBirth": "2020-05-15"}
    put_response = client.put("/hello/guido", json=payload)
    assert put_response.status_code == 204
    get_response = client.get("/hello/guido")
    assert get_response.status_code == 200
    assert get_response.json() == {"message": "Hello, guido! Happy birthday!"}


@freeze_time("2022-05-15 12:00")
def test_future_birthday(client):
    payload = {"dateOfBirth": "2022-06-01"}
    response = client.put("/hello/guido", json=payload)
    assert response.status_code == 400
    assert response.json() == {"detail": "Birthday is in the future"}


def test_non_apha_username(client):
    payload = {"dateOfBirth": "2022-06-01"}
    response = client.put("/hello/abc123", json=payload)
    assert response.status_code == 400
    assert response.json() == {"detail": "Username must contain only letters"}
