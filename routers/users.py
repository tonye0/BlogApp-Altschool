from fastapi import APIRouter, Depends, HTTPException, status
from schemas.user import * 
from database import models
from database.database_connection import engine, get_db
from sqlalchemy.orm import Session
from services.user_service import PasswordHasher
from dependencies.OAuth2 import get_current_user
from services.user_service import UserService


user_router = APIRouter()

user = UserService()

models.Base.metadata.create_all(engine)



@user_router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(req: UserCreate, db: Session = Depends(get_db)):
    
    return user.register(req, db)
    


@user_router.get("/{id}", status_code=status.HTTP_200_OK, response_model=User) 
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    
    return user.get_user(id, db)
    


@user_router.put("/{id}/update", status_code=status.HTTP_200_OK)
def update_user(id: int, req: UpdateUser, db: Session = Depends(get_db), current_user: UserLogin = Depends(get_current_user)):
    
    return user.update(id, req, db)