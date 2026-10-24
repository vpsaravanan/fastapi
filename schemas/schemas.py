# schemas.py
from pydantic import BaseModel

# Common properties shared across creation and reading
class UserBase(BaseModel):
    name: str
    email: str
    password:str
    aadhar_number:str

# Schema used for creating a user (inputs from client)
class UserCreate(UserBase):
    pass

# Schema used for returning a user (outputs to client)
class UserResponse(UserBase):
    id: int
    is_active: bool
    aadhar_number: str

    class Config:
        from_attributes = True  # Tells Pydantic to read data even if it's an ORM model
