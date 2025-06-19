from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session
from models.database import get_db
from models.models import Job
from fastapi.templating import Jinja2Templates
import os

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))


# Проверяет куку is_admin (доступ только админам)
# Получает все вакансии из БД
# Рендерит HTML-шаблон dashboard.html с списком вакансий
@router.get("/admin/dashboard", response_class=HTMLResponse)
async def admin_dashboard(request: Request, db: Session = Depends(get_db)):
    if not request.cookies.get("is_admin"):
        raise HTTPException(status_code=403)
    
    jobs = db.query(Job).all()
    return templates.TemplateResponse("admin/dashboard.html", {
        "request": request,
        "jobs": jobs
    })


# Принимает данные из HTML-формы
# Создаёт новую вакансию в БД
# Перенаправляет обратно на дашборд
@router.post("/admin/jobs/add")
async def add_job(
    request: Request,
    title: str = Form(...),
    description: str = Form(...),
    db: Session = Depends(get_db)
):
    if not request.cookies.get("is_admin"):
        raise HTTPException(status_code=403)
    
    if not title or not description:
        jobs = db.query(Job).all()
        return templates.TemplateResponse("admin/dashboard.html", {
            "request": request,
            "jobs": jobs,
            "error": "Все поля обязательны для заполнения"
        })
    
    db_job = Job(title=title, description=description)
    db.add(db_job)
    db.commit()
    return RedirectResponse(url="/admin/dashboard", status_code=303)


# Удаляет вакансию по ID
# Возвращает на дашборд
@router.post("/admin/jobs/delete/{job_id}")
async def delete_job(
    request: Request,
    job_id: int,
    db: Session = Depends(get_db)
):
    if not request.cookies.get("is_admin"):
        raise HTTPException(status_code=403)
    
    job = db.query(Job).filter(Job.id == job_id).first()
    if job:
        db.delete(job)
        db.commit()
    return RedirectResponse(url="/admin/dashboard", status_code=303)