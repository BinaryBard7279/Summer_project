from sqlalchemy import create_engine # создание движка (он управляет соединениями и Отвечает за подключение к БД)
from sqlalchemy.ext.declarative import declarative_base # Позволяет описывать таблицы БД в виде Python-классов (ORM-моделей).
from sqlalchemy.orm import sessionmaker # для создания сессий БД

DATABASE_URL = "sqlite:///./test.db" # подключения к БД
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}) # движок для работы с БД
Base = declarative_base() # класс для всех ORM-моделей/ При наследовании от Base класс становится моделью SQLAlchemy
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # сессии

# это соединение с БД
def get_db(): # это "временное подключение к базе данных" для одного запроса
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# get_db() - Даёт подключение к БД, когда нужно./ Закрывает его, даже если произошла ошибка