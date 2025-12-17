from sqlalchemy import Column, Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Session, relationship
from attrs import define
from .database import Base

from app.post_repository import Post

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    phone = Column(String, unique=True)
    password = Column(String)
    name = Column(String)
    city = Column(String)
    
    posts = relationship("Post", back_populates="owner")


@define
class UserCreate:
    username: str
    phone: str
    password: str
    name: str
    city: str

@define
class UserUpdate:
    phone: str
    name: str
    city: str


class UserRepo:
    def get_user_by_id(self, db: Session, user_id: int) -> User:
        return db.query(User).filter(User.id == user_id).first()
    
    def update_user_info(self, db: Session, user_id: int, user_info: UserUpdate) -> User | None:
        current_user = self.get_user_by_id(db, user_id=user_id)
        if not current_user:
            return None
        current_user.phone = user_info.phone
        current_user.name = user_info.name
        current_user.city = user_info.city
        db.commit()
        db.refresh(current_user)
        return current_user

    def get_user_by_username(self, db: Session, username: str) -> User | None:
        return db.query(User).filter(User.username == username).first()

    def add_user(self, db: Session, user: UserCreate) -> User:
        db_user = User(username=user.username, phone=user.phone, password=user.password, name=user.name, city=user.city)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user