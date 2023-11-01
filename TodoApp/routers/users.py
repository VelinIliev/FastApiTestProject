from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from passlib.context import CryptContext
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status

from database import SessionLocal
from models import Users
from .auth import get_current_user

router = APIRouter(
    prefix='/users',
    tags=['users']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


@router.get("/", status_code=status.HTTP_200_OK)
async def view_profile(user: user_dependency, db: db_dependency):
    if not user:
        raise HTTPException(status_code=401, detail='Authentication failed')

    current_user = db.query(Users).filter(Users.id == user.get('id')).first()

    return current_user


class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=3)


@router.put("/change-password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency, user_verification: UserVerification):
    if not user:
        raise HTTPException(status_code=401, detail='Authentication failed')

    current_user = db.query(Users).filter(Users.id == user.get('id')).first()

    if not bcrypt_context.verify(user_verification.password, current_user.password):
        raise HTTPException(status_code=401, detail='Error on password change')

    current_user.password = bcrypt_context.hash(user_verification.new_password)

    db.add(current_user)
    db.commit()


class PhoneVerification(BaseModel):
    phone_number: str = Field(min_length=2, max_length=11)


@router.put("/change-phone", status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number(user: user_dependency, db: db_dependency, phone_verification: PhoneVerification):
    if not user:
        raise HTTPException(status_code=401, detail='Authentication failed')

    current_user = db.query(Users).filter(Users.id == user.get('id')).first()

    current_user.phone_number = phone_verification.phone_number

    db.add(current_user)
    db.commit()
