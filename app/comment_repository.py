from sqlalchemy import Column, Boolean, ForeignKey, Integer, String, Float, delete, DateTime, func
from sqlalchemy.orm import Session, relationship
from attrs import define
from .database import Base

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    created_at = Column(DateTime(timezone=True), nullable=True)

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
    def get_all_comments_by_post_id(self, db: Session, post_id: int):
        return db.query(Comment).filter(Comment.post_id == post_id).all()
    def get_comment_by_id_for_post(self, db: Session, comment_id: int, post_id: int):
        return db.query(Comment).filter(Comment.post_id == post_id, Comment.id == comment_id).one_or_none()
        
    def modify_comment(self, db: Session, comment_id: int, comment: CommentAttrs, owner_id: int):
        current_comment = self.get_comment_by_id_for_post(db, comment_id, comment.post_id)
        print(current_comment)
        print(owner_id)
        if not current_comment or current_comment.owner_id != owner_id:
            return None
        current_comment.content = comment.content
        db.commit()
        db.refresh(current_comment)
        return current_comment

    def delete_comment(self, db: Session, comment_id: int, owner_id: int, post_id: int) -> bool:
        deleted_comment = self.get_comment_by_id_for_post(db, comment_id, post_id)
        if not deleted_comment or deleted_comment.owner_id != owner_id:
            return False
        comment = db.query(Comment).filter(Comment.post_id == post_id, Comment.id == comment_id).delete(synchronize_session=False)
        db.commit()
        return comment == 1        
        

