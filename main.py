from fastapi import FastAPI
from routers.articles import article_router
from routers.users import user_router
from routers.login import login_router




app = FastAPI()

app.include_router(login_router, prefix= "/login", tags=["Login"])
app.include_router(user_router, prefix="/user", tags=["Users"])
app.include_router(article_router, prefix="/article", tags=["Articles"])



@app.get("/", tags=["HomePage"])
def homepage():
    return {"message": "welcome to my Blog app"}


@app.get("/about", tags=["HomePage"])
def about():
    return {
        "message": "This is my first major build with fastApi. More to come. No one can stop this moving train"
        }
    
@app.get("/contact", tags=["HomePage"])
def contact():
    return {
        "message": "Contact info"
        }


