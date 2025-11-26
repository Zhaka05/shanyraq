from sqlalchemy import Column, Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Session
from attrs import define
from .database import Base
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    phone = Column(String, unique=True)
    password = Column(String)
    name = Column(String)
    city = Column(String)

    # posts
    # comments
@define
class UserCreate:
    username: str
    phone: str
    password: str
    name: str
    city: str

class UserRepo:
    def add_user(self, db: Session, user: UserCreate):
        db_user = User(username=user.username, phone=user.phone, password=user.password, name=user.name, city=user.city)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user


