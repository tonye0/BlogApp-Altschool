from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import models
from schemas.user import * 


class ArticleService:
    
    def create(self, req, db: Session):
        new_article = models.Article(title = req.title, article_content = req.article_content, author_username = req.author_username)
    
        username = db.query(models.User).filter((models.User.username == req.author_username)).first()
        
        if not username:
            return HTTPException(
                status_code=status.HTTP_409_CONFLICT, 
                detail="There is no author with that username. Please check your username."
            )
        
        db.add(new_article)
        db.commit()
        db.refresh(new_article)
        
        article = {
        "message": "You have sucessfully published your article",
        "Details":{
            "Username": req.author_username,
            "Title": req.title,
            "Content": req.article_content,
            "Date": new_article.created_at,
            "Article ID": new_article.id
            }
        }
    
        return article

    
    def update(self, id: int, req, db: Session):
        
        article_update = db.query(models.Article).filter(models.Article.id == id)
    
        if not article_update.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Article not found.")
        
        article_update.update(req.dict()) 
        
        db.commit()
        

        return {
        "message": "Article updated sucessfully",
            "Updated article": {
                "Title": req.title, 
                "Content": req.article_content,
            }            
        }
        
    def delete(self, id: int, db: Session):
        article_delete = db.query(models.Article).filter(models.Article.id == id)
    
        if not article_delete.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Article not found.")

        article_delete.delete(synchronize_session=False)
        
        db.commit()
        
        return "Article deleted sucesfully"
    
    def show_articles(self, db):
        articles = db.query(models.Article).all()   
 
        return articles
        
    
    def get_article(self, id: int, db: Session):
        author = db.query(models.Article).filter(models.Article.id == id).first()
        if not author:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
        return author