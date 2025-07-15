from pydantic import BaseModel, Field


class UserBase(BaseModel):
    username: str = Field(..., example="DELMAT")
    email: str = Field(..., example="azangueleonel9@gmail.com")
    phone_number: str = Field(..., example="+237 657450314")
    hashed_password : str = Field(..., example="hashed_password")
    role : str = Field(..., example="admin")  # e.g., "admin" or "user"
    is_active : bool = Field(..., example=True)

class UserCreate(UserBase):
    pass

