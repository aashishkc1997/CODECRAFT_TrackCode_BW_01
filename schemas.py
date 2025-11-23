from pydantic import BaseModel, EmailStr

# Shared fields
class UserBase(BaseModel):
    name: str
    email: EmailStr
    age: int

# For creating user (no id)
class UserCreate(UserBase):
    pass

# Response model (includes id)
class User(UserBase):
    id: str

    model_config = {
        "from_attributes": True
    }
class EmailResponse(BaseModel):
    email: EmailStr