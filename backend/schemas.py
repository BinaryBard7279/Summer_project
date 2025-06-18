from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    fio: str
    specialty: str
    course: int
    record_book: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class JobBase(BaseModel):
    title: str
    description: str
    deadline_in_days: int
    money: int

class JobCreate(JobBase):
    pass

class Job(JobBase):
    id: int

    class Config:
        orm_mode = True