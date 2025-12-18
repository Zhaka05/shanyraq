from sqlalchemy import Column, Boolean, ForeignKey, Integer, String, Float, delete
from sqlalchemy.orm import Session, relationship
from attrs import define
from .database import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)
    price = Column(Integer)
    address = Column(String)
    area = Column(Float)
    rooms_count = Column(Integer)
    description = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")


@define
class PostAttrs:
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str


class PostRepo:
    def get_post_by_id(self, db: Session, post_id: int) -> Post:
        return db.query(Post).filter(Post.id == post_id).first()
    def get_post_by_id_for_owner(self, db: Session, post_id: int, owner_id: int) -> Post:
        return db.query(Post).filter(Post.id == post_id, Post.owner_id == owner_id).first()
    # def update_user_info(self, db: Session, post_id: int, post_info: PostUpdate) -> Post:
    #     current_post = self.get_user_by_id(db, post_id=post_id)
    #     if not current_post:
    #         return None
    #     current_post.phone = post_info.phone
    #     current_post.name = post_info.name
    #     current_post.city = post_info.city
    #     db.commit()
    #     db.refresh(current_post)
    #     return current_post

    # def get_user_by_username(self, db: Session, username: str) -> Post | None:
    #     return db.query(Post).filter(Post.username == username).first()

    def add_post(self, db: Session, post: PostAttrs, owner_id: int) -> Post:
        db_post = Post(
            type=post.type,
            price=post.price,
            address=post.address,
            area=post.area,
            rooms_count=post.rooms_count,
            description=post.description,
            owner_id=owner_id,
        )
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        return db_post
    
    def update_post(self, db: Session, post_id: int, post: PostAttrs, owned_id: int) -> Post | None:
        current_post = self.get_post_by_id_for_owner(db, post_id, owned_id)
        if not current_post:
            return None
        current_post.type = post.type
        current_post.price = post.price
        current_post.address = post.address
        current_post.area = post.area
        current_post.rooms_count = post.rooms_count
        current_post.description = post.description
        db.commit()
        db.refresh(current_post)
        return current_post
    def delete_post(self, db: Session, post_id: int, owned_id: int) -> bool:
        post = db.query(Post).filter(Post.id == post_id, Post.owner_id == owned_id).delete(synchronize_session=False)
        db.commit()
        return post == 1
        
        

