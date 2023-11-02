from fastapi import APIRouter, Depends, HTTPException, status
from schemas.article import *
from database import models
from database.database_connection import engine, get_db
from sqlalchemy.orm import Session
from dependencies.OAuth2 import get_current_user
from schemas.user import UserLogin
from services.article_service import ArticleService


article_router = APIRouter()

article = ArticleService()

models.Base.metadata.create_all(engine)


@article_router.post("/create", status_code=status.HTTP_201_CREATED, description="Take note of the created article Id")
def create_article(req: CreateArticle, db: Session = Depends(get_db), current_user: UserLogin = Depends(get_current_user)):

    return article.create(req, db)


@article_router.put("/{id}/update", status_code=status.HTTP_200_OK)
def update_article(id: int, req: UpdateArticle, db: Session = Depends(get_db), current_user: UserLogin = Depends(get_current_user)):

    return article.update(id, req, db)


@article_router.delete("/{id}/delete", status_code=status.HTTP_204_NO_CONTENT)
def delete_article(id: int, db: Session = Depends(get_db), current_user: UserLogin = Depends(get_current_user),):

    return article.delete(id, db)


@article_router.get("/all-articles", status_code=status.HTTP_200_OK)
def show_all_articles(db: Session = Depends(get_db)):

    return article.show_articles(db)


@article_router.get("/{id}", status_code=status.HTTP_200_OK, response_model=DisplayArticle)
def get_articles_by_id(id: int, db: Session = Depends(get_db)):

    return article.get_article(id, db)
