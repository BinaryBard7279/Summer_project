from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from models.database import get_db
from models.models import User
from fastapi.templating import Jinja2Templates
import os
import logging

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # Настройка для хэширования паролей
logger = logging.getLogger(__name__) # Настройка логирования для записи ошибок

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"


# отображает HTML-форму входа
@router.get("/user/login", response_class=HTMLResponse)
async def user_login_page(request: Request):
    return templates.TemplateResponse("user/login.html", {"request": request})


# бработка входа
@router.post("/user/login")
async def user_login(
    request: Request,
    record_book: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    # Проверка заполнения полей
    if not record_book or not password:
        return templates.TemplateResponse("user/login.html", {
            "request": request,
            "error": "Все поля обязательны для заполнения"
        })
    # Поиск пользователя в БД
    user = db.query(User).filter(User.record_book == record_book).first()
    # Проверка пароля
    if not user or not pwd_context.verify(password, user.password_hash):
        return templates.TemplateResponse("user/login.html", {
            "request": request,
            "error": "Неверный номер зачетки или пароль"
        })
    # Успешный вход
    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie(key="user_id", value=str(user.id))
    return response


# вход админа
@router.get("/admin/login", response_class=HTMLResponse)
async def admin_login_page(request: Request):
    return templates.TemplateResponse("admin/login.html", {"request": request})


# Обработка входа
@router.post("/admin/login")
async def admin_login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    if not username or not password:
        return templates.TemplateResponse("admin/login.html", {
            "request": request,
            "error": "Все поля обязательны для заполнения"
        })
    
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        response = RedirectResponse(url="/admin/dashboard", status_code=303)
        response.set_cookie(key="is_admin", value="true")
        return response
    
    return templates.TemplateResponse("admin/login.html", {
        "request": request,
        "error": "Неверные учетные данные"
    })


# Выход из системы
@router.get("/logout")
async def logout():
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie("user_id")
    response.delete_cookie("is_admin")
    return response