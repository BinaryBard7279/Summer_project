# регистрации пользователей
from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from models.database import get_db
from models.models import User
from fastapi.templating import Jinja2Templates
import os
import logging

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))


# Отображение формы регистрации 
@router.get("/user/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("user/register.html", {"request": request})


# Обработка регистрации
@router.post("/user/register")
async def register_user(
    request: Request,
    fio: str = Form(...),
    specialty: str = Form(...),
    course: str = Form(...),
    record_book: str = Form(...),
    contacts: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    db: Session = Depends(get_db)
):
    if not all([fio, specialty, course, record_book, contacts, password, confirm_password]):
        return templates.TemplateResponse("user/register.html", {
            "request": request,
            "error": "Все поля обязательны для заполнения"
        })
    
    if password != confirm_password:
        return templates.TemplateResponse("user/register.html", {
            "request": request,
            "error": "Пароли не совпадают"
        })
    
    existing_user = db.query(User).filter(User.record_book == record_book).first()
    if existing_user:
        return templates.TemplateResponse("user/register.html", {
            "request": request,
            "error": "Пользователь с таким номером зачетки уже существует"
        })
    
    try:
        new_user = User(
            fio=fio,
            specialty=specialty,
            course=int(course),
            record_book=record_book,
            contacts=contacts,
            password_hash=pwd_context.hash(password)
        )
        
        db.add(new_user)
        db.commit()
        
        response = RedirectResponse(url="/", status_code=303)
        response.set_cookie(key="user_id", value=str(new_user.id))
        return response
    except Exception as e:
        logger.error(f"Error during registration: {str(e)}")
        return templates.TemplateResponse("user/register.html", {
            "request": request,
            "error": "Произошла ошибка при регистрации"
        })