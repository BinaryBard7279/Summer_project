from fastapi import FastAPI, Request, Depends, HTTPException, status, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import List, Optional

from . import models, schemas, crud, auth
from .database import SessionLocal, engine
from .config import settings

# Инициализация приложения
app = FastAPI(title="Студенческая фриланс-биржа")

# Настройка статических файлов и шаблонов
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Создание таблиц в БД
models.Base.metadata.create_all(bind=engine)

# Dependency для получения сессии БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Создание администратора при первом запуске
@app.on_event("startup")
async def startup():
    db = SessionLocal()
    try:
        if not crud.get_user_by_username(db, "admin"):
            admin_user = schemas.UserCreate(
                username="admin",
                email="admin@example.com",
                full_name="Admin",
                course=0,
                specialty="Admin",
                password="admin123"
            )
            created_user = crud.create_user(db, admin_user)
            # Делаем пользователя администратором
            created_user.is_admin = True
            db.commit()
    finally:
        db.close()

# Регистрация и аутентификация
@app.post("/api/register", response_model=schemas.User)
def api_register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email уже зарегистрирован")
    return crud.create_user(db=db, user=user)

@app.post("/api/token")
def api_login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Работа с кейсами
@app.post("/api/cases/", response_model=schemas.Case)
def api_create_case(
    case: schemas.CaseCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_admin_user)
):
    return crud.create_case(db=db, case=case, owner_id=current_user.id)

@app.get("/api/cases/", response_model=List[schemas.Case])
def api_read_cases(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cases = crud.get_cases(db, skip=skip, limit=limit)
    return cases

@app.get("/api/cases/{case_id}", response_model=schemas.CaseWithResponses)
def api_read_case(case_id: int, db: Session = Depends(get_db)):
    case = crud.get_case(db, case_id=case_id)
    if case is None:
        raise HTTPException(status_code=404, detail="Кейс не найден")
    return case

# Отклики на кейсы
@app.post("/api/cases/{case_id}/respond", response_model=schemas.Response)
def api_respond_to_case(
    case_id: int,
    response: schemas.ResponseCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    return crud.create_response(db=db, response=response, user_id=current_user.id, case_id=case_id)

# Фронтенд эндпоинты
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, db: Session = Depends(get_db)):
    cases = crud.get_cases(db)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "cases": cases,
        "current_user": None  # Здесь будет текущий пользователь после аутентификации
    })

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = auth.authenticate_user(db, username, password)
    if not user:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Неверное имя пользователя или пароль"
        })
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
    return response

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
async def register(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    full_name: str = Form(...),
    course: int = Form(...),
    specialty: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user_data = schemas.UserCreate(
        username=username,
        email=email,
        full_name=full_name,
        course=course,
        specialty=specialty,
        password=password
    )
    
    try:
        user = crud.create_user(db, user_data)
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    except Exception as e:
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": str(e)
        })

@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/")
    response.delete_cookie("access_token")
    return response

@app.get("/cases/{case_id}", response_class=HTMLResponse)
async def case_detail(request: Request, case_id: int, db: Session = Depends(get_db)):
    case = crud.get_case(db, case_id=case_id)
    if case is None:
        raise HTTPException(status_code=404, detail="Кейс не найден")
    
    return templates.TemplateResponse("case_detail.html", {
        "request": request,
        "case": case,
        "current_user": None  # Здесь будет текущий пользователь после аутентификации
    })

@app.get("/admin", response_class=HTMLResponse)
async def admin_panel(
    request: Request,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_admin_user)
):
    cases = crud.get_cases(db)
    users = crud.get_users(db)
    return templates.TemplateResponse("admin.html", {
        "request": request,
        "cases": cases,
        "users": users,
        "current_user": current_user
    })