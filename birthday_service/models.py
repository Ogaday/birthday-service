from sqlalchemy import Column, Date, Integer, String

from birthday_service.database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String(), unique=True, nullable=False)
    date_of_birth = Column(Date, nullable=False)

    def __repr__(self):
        return f"User(id={self.id}, name={self.name})"
