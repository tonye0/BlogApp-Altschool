from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from database.database_connection import Base
from datetime import datetime




class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String, unique=True) 
    email = Column(String) 
    password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    articles = relationship("Article", back_populates="author")

   
class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    article_content = Column(String)
    author_username = Column(String, ForeignKey("users.username"))
    created_at = Column(DateTime, default=datetime.utcnow)  
    
    author = relationship("User", back_populates="articles")
  
    

    