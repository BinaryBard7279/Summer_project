# Это endpoint, который позволяет авторизованным пользователям оставлять отклики на вакансии 
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from models.database import get_db
from models.models import Response

router = APIRouter()



@router.post("/jobs/respond/{job_id}")
async def respond_to_job(
    request: Request,
    job_id: int,
    db: Session = Depends(get_db)
):
    user_id = request.cookies.get("user_id")
    if not user_id:
        raise HTTPException(status_code=403)
    
    db_response = Response(
        user_id=int(user_id),
        job_id=job_id,
        message="Хочу участвовать в этом проекте!"
    )
    db.add(db_response)
    db.commit()
    return RedirectResponse(url="/", status_code=303)