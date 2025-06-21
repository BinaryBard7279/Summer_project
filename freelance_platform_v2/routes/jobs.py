from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from models.database import get_db
from models.models import User, Job, Response

router = APIRouter()

@router.post("/jobs/respond/{job_id}")
async def respond_to_job(
    request: Request,
    job_id: int,
    db: Session = Depends(get_db)
):
    user_id = request.cookies.get("user_id")
    if not user_id:
        raise HTTPException(status_code=403, detail="Требуется авторизация")
    
    user = db.query(User).filter(User.id == int(user_id)).first()
    job = db.query(Job).filter(Job.id == job_id).first()
    
    if not user or not job:
        raise HTTPException(status_code=404, detail="Не найдено")
    
    # Проверка на существующий отклик
    if db.query(Response).filter_by(user_id=user.id, job_id=job.id).first():
        return RedirectResponse(url="/?error=Вы+уже+откликались", status_code=303)
    
    # Создаем новый отклик
    db.add(Response(user_id=user.id, job_id=job.id))
    db.commit()
    
    return RedirectResponse(url="/?success=Отклик+отправлен", status_code=303)