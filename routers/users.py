from fastapi import APIRouter, Depends, HTTPException, status
from schemas.user import * 
from database import models
from database.database_connection import engine, SessionLocal
from sqlalchemy.orm import Session
from validate_email import validate_email
from services.user_service import PasswordHasher
from dependencies.OAuth2 import get_current_user


user_router = APIRouter()

models.Base.metadata.create_all(engine)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@user_router.post("/register", status_code=status.HTTP_201_CREATED)
def create_user(req: UserCreate, db: Session = Depends(get_db)):
    
    is_valid = validate_email(req.email)
    
    if not is_valid:
        return HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST, 
            detail="Invalid email address. Please provide a valid email."
        )
        
    # Check if the email or username already exists in the database
    existing_username = db.query(models.User).filter((models.User.username == req.username)).first()
    if existing_username:
        return HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="Username is already in use. Please choose a different username."
        )
    
    existing_email = db.query(models.User).filter((models.User.email == req.email)).first()
    if existing_email:
        return HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="Email is already in registered. Please choose a different email."
        )

    hashed_password = PasswordHasher.get_password_hash(req.password)
    new_user = models.User(
        first_name = req.first_name, 
        last_name = req.last_name, 
        username = req.username, 
        email = req.email, 
        password = hashed_password
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    new_profile = {
        "First name": req.first_name,
        "Last name": req.last_name,
        "Username": req.username,
        "Email": req.email
    }
    return {
        "message": "Thank you for registering.",
        "Profile": new_profile
        }    

@user_router.get("/{id}", status_code=status.HTTP_200_OK, response_model=User) 
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There is no user with the id {id}")
    return user


@user_router.put("/{id}/update", status_code=status.HTTP_200_OK)
def update_user(id: int, req: UpdateUser, db: Session = Depends(get_db), current_user: UserLogin = Depends(get_current_user)):
    is_valid = validate_email(req.email)
    
    if not is_valid:
        return HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST, 
            detail="Invalid email address. Please provide a valid email."
        )
        
    user_update = db.query(models.User).filter(models.User.id == id)
 
    if not user_update.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "User not found.")
    
    user_update.update(req.dict()) 
    
    db.commit()
    
    updated_profile = {
        "First name": req.first_name,
        "Last name": req.last_name,
        "Username": req.username,
        "Email": req.email
    }
   
    return {
        "message": "Update sucessful",
        "Updated profile": updated_profile
    }



