from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import models
from schemas.user import * 
from passlib.context import CryptContext
from validate_email import validate_email



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PasswordHasher():
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)
    
    
class UserService:
    
    def register(self, req, db: Session):
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
            password = hashed_password,
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        
        new_profile = {
            "Name": f"{req.first_name} {req.last_name}",            "Username": req.username,
            "Email": req.email,
        }
        
        return {
            "message": "Thank you for registering.",
            "Profile": new_profile
            }
    
      
    def get_user(self, username: str, db: Session):
        
        user = db.query(models.User).filter(models.User.username == username).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There is no user with the username {username}")
        return user
    
    
    def update(self, username: str, req, db: Session):
        
        user_update = db.query(models.User).filter(models.User.username == username)
    
        if not user_update.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"User with username {username} not found.")
         
        
        is_valid = validate_email(req.email)
        
        if not is_valid:
            return HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST, 
                detail="Invalid email address. Please provide a valid email."
            )
            
      
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
        
        