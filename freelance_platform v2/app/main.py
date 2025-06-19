from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles # импорт класса для работы со статическими файлами
from fastapi.templating import Jinja2Templates # шаблонизатор Jinja2
from sqlalchemy.orm import Session # класс (супер) для работы с сессиями SQLAlchemy (запросы к БД)
import os # работа с файловой системой (эта хуйня так-то не нужна)

from models.database import engine, Base, get_db # engine – движок SQLAlchemy для подключения к БД/
from models.models import Job # импорт модели таблицы "Задания" из БД
from routes import auth, admin, jobs, users # импорт auth – аутентификация, admin – админ-панель, jobs – работа с заданиями, users – управление пользователями.

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # переменная, которая содержит путь к папке, где находится исполняемый Python-файл.
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "../templates"))

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "../static")), name="static")

# подключение роутеров
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(jobs.router)
app.include_router(users.router)

# инициализация БД
Base.metadata.create_all(bind=engine)

@app.get("/")
async def read_root(request: Request, db: Session = Depends(get_db)):
    jobs = db.query(Job).all() # SQL-запрос: "получить все записи из таблицы Job"
    return templates.TemplateResponse("index.html", {"request": request, "jobs": jobs})