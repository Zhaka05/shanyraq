from fastapi import FastAPI, Form, Depends
from fastapi.responses import Response
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

# repository
from app.user_repository import UserRepo, UserCreate, User

#database
from .database import Base, SessionLocal, engine

Base.metadata.create_all(bind=engine) # for creation of all tables

# database
from sqlalchemy.orm import Session

app = FastAPI()
users_repo = UserRepo()

oauth2 = OAuth2PasswordBearer(tokenUrl="")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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
    
    


    
