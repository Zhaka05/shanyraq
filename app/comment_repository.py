from sqlalchemy import Column, Boolean, ForeignKey, Integer, String, Float, delete
from sqlalchemy.orm import Session, relationship
from attrs import define
from .database import Base

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))

    owner = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")

@define
class CommentAttrs:
    content: str
    post_id: int

class CommentRepo:
    def get_comment_by_id(self, db: Session, comment_id: int) -> Comment | None:
        return db.query(Comment).filter(Comment.id == comment_id).first()
    def add_comment(self, db: Session, comment: CommentAttrs, owner_id: int) -> Comment:
        db_comment = Comment(
            content=comment.content,
            owner_id=owner_id,
            post_id=comment.post_id,
        )
        db.add(db_comment)
        db.commit()
        db.refresh(db_comment)
        return db_comment



