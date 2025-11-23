from fastapi import FastAPI, HTTPException
from typing import List, Dict
from uuid import uuid4
from pydantic import BaseModel, EmailStr

app = FastAPI()

# ==========================
# Pydantic Schemas
# ==========================

class UserBase(BaseModel):
    name: str
    email: EmailStr
    age: int

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: str

class EmailResponse(BaseModel):
    email: EmailStr


# ==========================
# In-memory HashMap storage
# ==========================

users: Dict[str, User] = {}   # key = id, value = User object


# ==========================
# REST API Endpoints
# ==========================

@app.get("/")
def root():
    return {"message": "Welcome to HashMap REST API"}


# CREATE USER
@app.post("/users", response_model=User)
def create_user(data: UserCreate):
    # check duplicate email
    for u in users.values():
        if u.email == data.email:
            raise HTTPException(status_code=400, detail="Email already exists")

    user_id = str(uuid4())
    new_user = User(id=user_id, **data.dict())
    users[user_id] = new_user
    return new_user


# READ ALL USERS
@app.get("/users", response_model=List[User])
def get_users():
    return list(users.values())

# UPDATE USER
@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: str, data: UserCreate):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")

    updated_user = User(id=user_id, **data.dict())
    users[user_id] = updated_user
    return updated_user


# DELETE USER
@app.delete("/users/{user_id}")
def delete_user(user_id: str):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")

    del users[user_id]
    return {"message": "User deleted"}
