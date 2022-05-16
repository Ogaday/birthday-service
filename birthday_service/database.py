from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from birthday_service import env

DSN = env("SQL_DSN", "sqlite:///./dummy.db")

engine = create_engine(DSN, echo=True)

SessionLocal = sessionmaker(bind=engine)

# Issue with dynamic base class typing:
Base = object
Base = declarative_base()  # type: ignore
