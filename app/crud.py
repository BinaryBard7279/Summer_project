from sqlalchemy.orm import Session
from . import models, schemas
from .database import SessionLocal  # Добавьте этот импорт
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Остальные функции остаются без изменений
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        course=user.course,
        specialty=user.specialty,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_case(db: Session, case_id: int):
    return db.query(models.Case).filter(models.Case.id == case_id).first()

def get_cases(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Case).filter(models.Case.is_active == True).offset(skip).limit(limit).all()

def create_case(db: Session, case: schemas.CaseCreate, owner_id: int):
    db_case = models.Case(**case.dict(), owner_id=owner_id)
    db.add(db_case)
    db.commit()
    db.refresh(db_case)
    return db_case

def create_response(db: Session, response: schemas.ResponseCreate, user_id: int, case_id: int):
    db_response = models.Response(
        message=response.message,
        user_id=user_id,
        case_id=case_id
    )
    db.add(db_response)
    db.commit()
    db.refresh(db_response)
    return db_response