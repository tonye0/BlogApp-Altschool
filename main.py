from fastapi import FastAPI, Depends
from routers.articles import article_router, show_all_articles
from routers.users import user_router
from routers.login import login_router

from database import models
from services.article_service import ArticleService
from database.database_connection import engine, get_db
from sqlalchemy.orm import Session

article = ArticleService()

app = FastAPI()

app.include_router(login_router, prefix= "/login", tags=["Login"])
app.include_router(user_router, prefix="/user", tags=["Users"])
app.include_router(article_router, prefix="/article", tags=["Articles"])

models.Base.metadata.create_all(engine)


@app.get("/", tags=["HomePage"])
def homepage():
    
    return {"message": "welcome to my Blog app"}

@app.get("/articles", tags=["HomePage"])
def articles(db: Session = Depends(get_db)):
    
    return  article.show_articles(db)
    

@app.get("/about", tags=["HomePage"])
def about():
    return {
        "message": "This is my first major build with fastApi. More to come. No one can stop this moving train"
        }
    
@app.get("/contact", tags=["HomePage"])
def contact():
    return {
        "message": "Here is my github profile : 'https://github.com/tonye0/'. Feel free to reach out."
        }
