from fastapi import FastAPI, Form
from fastapi.responses import Response
from pydantic import BaseModel

# repository
app = FastAPI()


class User(BaseModel):
    username: str
    phone: str
    password: str
    name: str
    city: str

@app.post("/registration")
def registration_get(user: User):
    pass
    
    
    
