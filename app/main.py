from fastapi import FastAPI, Form, Depends, HTTPException
from fastapi.responses import Response
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from jose import jwt

# repository
from app.user_repository import UserRepo, UserCreate, User, UserUpdate

#database
from .database import Base, SessionLocal, engine

Base.metadata.create_all(bind=engine) # for creation of all tables

# database
from sqlalchemy.orm import Session

app = FastAPI()
users_repo = UserRepo()

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
    user_id = decode_access_token(token)
    users_repo.update_user_info(db, user_id, UserUpdate(phone=user_update.phone, name=user_update.name, city=user_update.city))
    return Response(status_code=200)