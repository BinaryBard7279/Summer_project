from sqlalchemy import Column, Integer, String, ForeignKey # создаёт колонки в таблице БД и типа данных
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class User(Base): # модель таблицы users в БД
    __tablename__ = "users" # название
    
    id = Column(Integer, primary_key=True, index=True) # id 
    fio = Column(String, nullable=False) # ФИО 
    specialty = Column(String, nullable=False) # специальность 
    course = Column(Integer, nullable=False) # курс
    record_book = Column(String, unique=True, nullable=False) # зачётка
    contacts = Column(String, unique=True, nullable=False) # контакнтые данные
    password_hash = Column(String, nullable=False) # хэш пароля
    
    responses = relationship("Response", back_populates="user")

class Job(Base): # модель таблицы Job в БД
    __tablename__ = "jobs" # название
    
    id = Column(Integer, primary_key=True, index=True) # id 
    title = Column(String, nullable=False) # название вакансии 
    description = Column(String, nullable=False) # описание вакансии
    srok = Column(Integer, nullable=False)
    money = Column(Integer, nullable=False)
    
    responses = relationship("Response", back_populates="job")

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Response(Base):
    __tablename__ = "responses"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))
    
    user = relationship("User", back_populates="responses")
    job = relationship("Job", back_populates="responses")