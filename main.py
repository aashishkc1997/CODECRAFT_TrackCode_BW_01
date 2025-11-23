from fastapi import FastAPI, HTTPException
from typing import Dict, List
from uuid import uuid4
import schemas

app = FastAPI()

# In-memory user store (HashMap)
users: Dict[str, schemas.User] = {}

@app.get("/")
def root():
    return {"message": "Welcome to my FastAPI app"}


# Create User
@app.post("/users", response_model=schemas.User)
def create_user(user_data: schemas.UserCreate):

    # Check duplicate email
    for u in users.values():
        if u.email == user_data.email:
            raise HTTPException(status_code=400, detail="Email already exists")

    user_id = str(uuid4())
    new_user = schemas.User(id=user_id, **user_data.dict())
    users[user_id] = new_user
    return new_user


# Get all users
@app.get("/users", response_model=List[schemas.User])
def get_users():
    return list(users.values())


# Get a single user
@app.get("/users/{user_id}", response_model=schemas.User)
def get_user(user_id: str):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    return users[user_id]


# Update a user
@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: str, data: schemas.UserCreate):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")

    updated_user = schemas.User(id=user_id, **data.dict())
    users[user_id] = updated_user
    return updated_user


# Delete User
@app.delete("/users/{user_id}")
def delete_user(user_id: str):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")

    del users[user_id]
    return {"message": "User deleted"}


# Get only emails
@app.get("/emails", response_model=List[schemas.EmailResponse])
def get_emails():
    return [{"email": u.email} for u in users.values()]
