from sqlalchemy import Column, Boolean, ForeignKey, Integer, String, Float
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


@define
class PostCreate:
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str

@define
class PostUpdate:
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str


class PostRepo:
    def get_post_by_id(self, db: Session, post_id: int) -> Post:
        return db.query(Post).filter(Post.id == post_id).first()
    
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

    def add_post(self, db: Session, post: PostCreate, owner_id: int) -> Post:
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