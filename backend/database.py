from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text

# Указываем URI для подключения к базе данных SQLite
DATABASE_URL = "sqlite+aiosqlite:///./database.db"

# Создаём объект движка
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Создаём объект Metadata
metadata = MetaData()

# Создаём базовый класс для определения моделей
Base = declarative_base()

# Определяем модель User
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    fio = Column(String, index=True)  # Фамилия и имя
    specialty = Column(String)          # Специальность
    course = Column(Integer)            # Курс
    record_book = Column(String)        # Номер зачетной книжки

# Определяем модель Job
class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)  # Название работы
    description = Column(Text)           # Описание работы