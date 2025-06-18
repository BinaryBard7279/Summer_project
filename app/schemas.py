from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    course: int
    specialty: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_admin: bool
    
    class Config:
        from_attributes = True

class CaseBase(BaseModel):
    title: str
    description: str
    deadline: datetime
    cost: float

class CaseCreate(CaseBase):
    pass

class Case(CaseBase):
    id: int
    created_at: datetime
    is_active: bool
    
    class Config:
        from_attributes = True

class ResponseBase(BaseModel):
    message: str

class ResponseCreate(ResponseBase):
    case_id: int

class Response(ResponseBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class CaseWithResponses(Case):
    responses: List[Response] = []