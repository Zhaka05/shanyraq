from sqlalchemy import Column, Boolean, ForeignKey, Integer, String, Float, delete
from sqlalchemy.orm import Session, relationship
from attrs import define
from .database import Base

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    comment = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))

    owner = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")
