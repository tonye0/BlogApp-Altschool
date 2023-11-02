from pydantic import BaseModel
from typing import List
from datetime import datetime
from schemas.article import DisplayArticle



class BaseUser(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str
    
    class Config:
        from_attributes = True
    
    
class User(BaseUser):
    articles: List[DisplayArticle] = []
    
    
    class Config:
        from_attributes = True
    



class UserCreate(BaseUser):   
    password: str

    
    class Config:
        from_attributes = True


class UpdateUser(BaseUser):
    class Config:
        from_attributes = True
   


class UserLogin(BaseModel):
    username: str
    password: str


class UserToken(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
