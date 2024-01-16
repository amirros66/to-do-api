from sqlalchemy.orm import Session
from passlib.context import CryptContext
from . import models, schemas
from app import auth 
from fastapi import HTTPException
 
#Storing passwords securely - hash them using bcrypt
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_hashed_password(password: str) -> str:
    return password_context.hash(password)

def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_hashed_password(user.password)
    db_user = models.User(username=user.username, password=hashed_password)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def login_user(db: Session, user: schemas.UserCredentials):
    db_user = db.query(models.User).filter(
        models.User.username == user.username).first()

    user_password_error = "Incorrect username or password"

    if db_user is None:
        raise HTTPException(status_code=404, detail=user_password_error)
    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail=user_password_error)
    return {
        "access_token": auth.create_access_token(f"{db_user.id}:{db_user.username}"), 
        "token_type": "bearer"}

