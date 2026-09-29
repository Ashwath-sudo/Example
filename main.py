# Save this in main.py temporarily
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class UserRequest(BaseModel):
    user_id: int
    email: str