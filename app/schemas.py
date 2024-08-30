from datetime import datetime
from typing import Annotated, Optional
from pydantic import BaseModel, EmailStr, conint

class PostBase(BaseModel):
    title: str
    body: str
    published: bool = True

        
class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
    
    class Config:
        from_attributes=True
        
class Post(BaseModel):
    id: int
    title: str
    owner_id: int
    owner: UserResponse
    class Config:
        from_attributes=True
        
class PostOut(BaseModel):
    Post: Post
    likes: int



class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
    
class LikeBase(BaseModel):
    post_id: int
    dir: Annotated[int, conint(ge=0, le=1)]