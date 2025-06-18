# backend/database.py

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, Text

DATABASE_URL = "sqlite+aiosqlite:///./database.db"

# Создаем асинхронный движок
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True
)

# Сессии для работы с базой данных
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    fio = Column(String, nullable=False)
    specialty = Column(String, nullable=False)
    course = Column(Integer, nullable=False)
    record_book = Column(String, unique=True, nullable=False)

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)

# Функция получения базы данных
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session