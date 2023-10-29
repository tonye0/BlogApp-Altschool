from fastapi import APIRouter, Depends, HTTPException, status
from schemas.article import * 
from database import models
from database.database_connection import engine, SessionLocal
from sqlalchemy.orm import Session, joinedload
from dependencies.OAuth2 import get_current_user
from schemas.user import UserLogin



article_router = APIRouter()

models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@article_router.post("/create", status_code=status.HTTP_201_CREATED, response_model= DisplayArticle, )
def create_article(req: CreateArticle, db: Session = Depends(get_db), current_user: UserLogin = Depends(get_current_user),):
    new_article = models.Article(title = req.title, article_content = req.article_content, author_id = req.author_id)
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article



@article_router.put("/{article_id}/update", status_code=status.HTTP_200_OK)
def update_article(id: int, req: UpdateArticle, db: Session = Depends(get_db), current_user: UserLogin = Depends(get_current_user)):
    article_update = db.query(models.Article).filter(models.Article.id == id)
    
    if not article_update.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Article not found.")
    
    article_update.update(req.dict()) 
    
    db.commit()
   
    return {
       "message": "Article updated sucessfully",
          "New update": {
              "Title": req.title, 
              "Content": req.article_content,
          }            
       }


@article_router.delete("/{article_id}/delete", status_code=status.HTTP_204_NO_CONTENT)
def delete_article(id: int, db: Session = Depends(get_db), current_user: UserLogin = Depends(get_current_user),):
    article_delete = db.query(models.Article).filter(models.Article.id == id)
    
    if not article_delete.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Article not found.")

    article_delete.delete(synchronize_session=False)
    db.commit()
    return "Article deleted sucesfully"
    



@article_router.get("/all-articles", status_code=status.HTTP_200_OK, response_model= list[DisplayArticle])
def show_all_articles(db: Session = Depends(get_db)):
    # articles = db.query(models.Article).all()   
    # return articles
    
    articles = db.query(models.Article).options(joinedload(models.Article.author)).all()
    return articles



@article_router.get("/by-id/{author_id}", status_code=status.HTTP_200_OK, response_model= DisplayArticle)
def get_articles_by_author(id: int, db: Session = Depends(get_db)):
    author = db.query(models.Article).filter(models.Article.id == id).first()
    if not author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Article with id {id}, not found")
    return author

