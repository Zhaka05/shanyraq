from fastapi import FastAPI, Form, Depends, HTTPException
from fastapi.responses import Response, JSONResponse
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from jose import jwt

# repository
from app.user_repository import UserRepo, UserCreate, User, UserUpdate
from app.post_repository import PostRepo, PostAttrs

#database
from .database import Base, SessionLocal, engine

Base.metadata.create_all(bind=engine) # for creation of all tables

# database
from sqlalchemy.orm import Session

app = FastAPI()
users_repo = UserRepo()
posts_repo = PostRepo()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/users/login")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_access_token(user_id: int) -> str:
    to_encode = {"user_id": str(user_id)}
    encoded_jwt = jwt.encode(to_encode, "some-secret", "HS256")
    return encoded_jwt

def decode_access_token(token: str) -> str:
    data = jwt.decode(token, "some-secret", "HS256")
    return data["user_id"]

class UserRequest(BaseModel):
    username: str
    phone: str
    password: str
    name: str
    city: str

@app.post("/auth/users/")
def post_user(user: UserRequest, db: Session = Depends(get_db)):
    users_repo.add_user(db, UserCreate(username=user.username, phone=user.phone, password=user.password, name=user.name, city=user.city))
    return Response(status_code=202)
    
@app.post("/auth/users/login")
def post_login_user(
    username: str = Form(),
    password: str = Form(),
    db: Session = Depends(get_db),
):  
    user = users_repo.get_user_by_username(db, username)
    if not user or user.password != password:
            return HTTPException(status_code=404, detail="Invalid password or username")

    token = create_access_token(int(user.id))
    return {"access_token": token}

class UserUpdateRequest(BaseModel):
    phone: str
    name: str
    city: str

@app.patch("/auth/users/me")
def patch_me(
    user_update: UserUpdateRequest,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    user_id = int(decode_access_token(token))
    users_repo.update_user_info(db, user_id, UserUpdate(phone=user_update.phone, name=user_update.name, city=user_update.city))
    return Response(status_code=200)

class UserGetResponse(BaseModel):
    id: int
    username: str
    phone: str
    password: str
    name: str
    city: str


@app.get("/auth/users/me", response_model=UserGetResponse)
def get_me(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    user_id = int(decode_access_token(token))
    user = users_repo.get_user_by_id(db, int(user_id))
    return UserGetResponse(id=user.id, username=user.username, phone=user.phone, password=user.password, name=user.name, city=user.city)

class PostAnnouncementRequest(BaseModel):
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str


@app.post("/shanyraks/")
def post_announcement(
    post_announcement: PostAnnouncementRequest,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    user_id = decode_access_token(token)
    post_create = PostAttrs(type=post_announcement.type, price=post_announcement.price, address=post_announcement.address, area=post_announcement.area, rooms_count=post_announcement.rooms_count, description=post_announcement.description)
    new_post = posts_repo.add_post(db, post_create, owner_id=int(user_id))
    return JSONResponse(content={"id": new_post.id}, status_code=200)

class AnnouncementGetResponse(BaseModel):
    id: int
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str
    owner_id: int

@app.get("/shanyraks/{id}", response_model=AnnouncementGetResponse)
def get_announcement(
    id: int,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    post = posts_repo.get_post_by_id(db, id)
    if not post:
        return HTTPException(status_code=404, detail={"error_message": "Post Not Found"})
    return AnnouncementGetResponse(
        id=post.id,
        type=post.type,
        price=post.price,
        address=post.address,
        area=post.area,
        rooms_count=post.rooms_count,
        description=post.description,
        owner_id=post.owner_id,
    )

@app.patch("/shanyraks/{id}")
def patch_announcement(
    post_update: PostAnnouncementRequest,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    user_id = decode_access_token(token)
    posts_repo.update_post(db, PostAttrs(
        type=post_update.type,
        price=post_update.price,
        address=post_update.address,
        area=post_update.area,
        rooms_count=post_update.rooms_count,
        description=post_update.description,
        ), int(user_id))
    return Response(status_code=200)
