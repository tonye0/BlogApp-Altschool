from pydantic import BaseModel
from datetime import datetime


class ArticleBase(BaseModel):
    title: str
    article_content: str
    
    class Config:
        from_attributes = True
    
class DisplayArticle(ArticleBase):
    # id: int
    created_at: datetime

    
class CreateArticle(ArticleBase):
    author_id: int
    pass
    # created_at: datetime
    
class UpdateArticle(ArticleBase):
    
    
    class Config:
        from_attributes = True


class DeleteArticle(BaseModel):
    id: int
