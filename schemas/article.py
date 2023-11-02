from pydantic import BaseModel
from datetime import datetime


class ArticleBase(BaseModel):
    title: str
    article_content: str

    class Config:
        from_attributes = True


class DisplayArticle(ArticleBase):
    pass


class CreateArticle(ArticleBase):
    author_username: str


class UpdateArticle(ArticleBase):

    class Config:
        from_attributes = True
