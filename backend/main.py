from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from database import Base, engine


app = FastAPI()

# Подключение папки для статических файлов
app.mount("/static", StaticFiles(directory="backend/static"), name="static")

# Инициализация Jinja2
templates = Jinja2Templates(directory="backend/templates")

# Создание БД
@app.on_event("startup")
async def startup():
    await conn.run_sync(Base.metadata.create_all)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})