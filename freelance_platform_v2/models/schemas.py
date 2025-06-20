from pydantic import BaseModel, EmailStr

# Валидация данных (проверка)

class UserBase(BaseModel):
    fio: str
    course: int
    specialty: str
    record_book: str

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    is_admin: bool

    class Config:
        from_attributes = True

class JobCreate(BaseModel):
    title: str
    description: str
    srok: str
    money: str

class JobOut(JobCreate):
    id: int
    created_by: int

    class Config:
        from_attributes = True

class ResponseCreate(BaseModel):
    job_id: int
    message: str

class ResponseOut(ResponseCreate):
    id: int
    user_id: int

    class Config:
        from_attributes = True

class LoginForm(BaseModel):
    record_book: str
    password: str