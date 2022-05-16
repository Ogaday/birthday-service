from datetime import date

import pytest
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker

from birthday_service.controllers import (
    NoUserError,
    create_or_update_user,
    get_user_by_name,
)
from birthday_service.models import User


@pytest.fixture
def dummy_engine():
    engine = create_engine("sqlite:///:memory:")
    meta = MetaData(bind=engine)
    meta.create_all(tables=[User.__table__])
    return engine


@pytest.fixture
def dummy_session(dummy_engine):
    Session = sessionmaker(bind=dummy_engine)
    session = Session()
    try:
        yield session
    finally:
        session.close()


def test_create_user(dummy_session):
    user = create_or_update_user(db=dummy_session, name="guido", dob=date(2000, 1, 1))
    assert user == dummy_session.query(User).one()


def test_update_user(dummy_session):
    create_or_update_user(db=dummy_session, name="guido", dob=date(2000, 1, 1))
    user = create_or_update_user(db=dummy_session, name="guido", dob=date(2000, 1, 10))
    assert user == dummy_session.query(User).one()


def test_get_user_by_name(dummy_session):
    user = User(name="guido", date_of_birth=date(2000, 1, 1))
    dummy_session.add(user)
    dummy_session.flush()
    dummy_session.commit()
    assert get_user_by_name(db=dummy_session, name="guido") is user


def test_get_user_by_name_raises_error(dummy_session):
    with pytest.raises(NoUserError):
        get_user_by_name(db=dummy_session, name="guido")
