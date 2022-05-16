from datetime import date

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

import birthday_service.models as models


class NoUserError(Exception):
    """
    Raised when a queried user does not exist.
    """


def get_user_by_name(db: Session, name: str) -> models.User:
    # what about if there is no existing user?
    try:
        user = db.query(models.User).filter(models.User.name == name.lower()).one()
    except NoResultFound as e:
        raise NoUserError from e
    return user


def create_or_update_user(db: Session, name: str, dob: date) -> models.User:
    try:
        with db.begin_nested():
            user = models.User(name=name.lower(), date_of_birth=dob)
            db.add(user)
            db.flush()
    except IntegrityError:
        user = db.query(models.User).filter(models.User.name == name.lower()).one()
        user.date_of_birth = dob
        db.add(user)
        db.flush()
    return user
