from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func
from app import oauth2
from .. import schemas, models, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List, Optional

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/", response_model=List[schemas.PostOut])
# @router.get("/")
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 100, skip: int = 0, search: Optional[str] = ""):
    
    posts = db.query(
        models.Post, func.count(models.Like.post_id).label("likes")
        ).join(
            models.Like, models.Like.post_id == models.Post.id, isouter=True
         ).group_by(
        models.Post.id
        ).filter(
            models.Post.title.contains(search)
        ).limit(limit).offset(skip).all()

    posts = list ( map (lambda x : x._mapping, posts) )
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostBase, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id=current_user.id, **post.model_dump()) 
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post



@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(
        models.Post, func.count(models.Like.post_id).label("likes")
        ).filter(
            models.Post.id == id
        ).join(
            models.Like, models.Like.post_id == models.Post.id, isouter=True
        ).group_by(
            models.Post.id
        ).first()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )
        
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == id)
    
    if not post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )
    
    if post.first().owner_id != int(current_user.id):    
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostBase, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    if post_query.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was not found",
        )

    if post_query.first().owner_id != int(current_user.id):    
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    
    return post_query.first()
