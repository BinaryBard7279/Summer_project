from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from python import models, database

app = FastAPI()

# Подключение к базе данных
database.Base.metadata.create_all(bind=database.engine)

# Настройка статических файлов
app.mount("/static", StaticFiles(directory="."), name="static")  # Используем "" для доступа к статическим файлам в корне проекта

# Функция для получения сессии базы данных
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Эндпоинт для создания пользователя
@app.post("/users/")
def create_user(name: str, email: str, db: Session = Depends(get_db)):
    user = models.User(name=name, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# Эндпоинт для получения всех пользователей
@app.get("/users/")
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users

# Эндпоинт для получения всех заказов
@app.get("/orders/")
def read_orders(db: Session = Depends(get_db)):
    orders = db.query(models.Order).all()  # Замени Order на свою модель заказа
    return orders

# Эндпоинт для индекса
@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("index.html", "r") as f:
        return f.read()