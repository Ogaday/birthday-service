from datetime import date, datetime

from fastapi import Depends, FastAPI, HTTPException, Response
from pydantic import BaseModel
from sqlalchemy.orm import Session

from birthday_service.birthday import next_birthday
from birthday_service.controllers import (
    NoUserError,
    create_or_update_user,
    get_user_by_name,
)
from birthday_service.database import SessionLocal, engine
from birthday_service.models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()


class DateOfBirth(BaseModel):
    dateOfBirth: date


class BirthdayResponse(BaseModel):
    message: str


def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    finally:
        db.close()


@app.get("/")
def root():
    """
    Application root and liveness endpoint.

    Returns current UTC time.
    """
    return {"utcnow": datetime.utcnow()}


@app.get("/hello/{username}")
def get_birthday_message(username: str, db: Session = Depends(get_db)):
    """
    Get a birthday message for the user.

    The response will greet the user with a custom birthday message if it is their
    birthday, otherwise it will return the number of days until their next birthday.
    """
    try:
        user = get_user_by_name(db=db, name=username)
        next_ = next_birthday(user.date_of_birth)
        if next_ == date.today():
            return {"message": f"Hello, {username}! Happy birthday!"}
        else:
            diff = (next_ - date.today()).days
            return {
                "message": f"Hello, {username}! Your birthday is in {diff} day{'s' if diff > 1 else ''}"
            }
    except NoUserError:
        raise HTTPException(status_code=404, detail="User not found")


@app.put("/hello/{username}", status_code=204, response_model=None)
def set_birthday(
    username: str, date_of_birth: DateOfBirth, db: Session = Depends(get_db)
):
    """
    Set the date of birth for the user.
    """
    if not username.isalpha():
        raise HTTPException(status_code=400, detail="Username must contain only letters")
    if date_of_birth.dateOfBirth >= date.today():
        raise HTTPException(status_code=400, detail="Birthday is in the future")
    create_or_update_user(db=db, name=username, dob=date_of_birth.dateOfBirth)
    return Response(status_code=204)
