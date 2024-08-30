from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from app import oauth2
from .. import schemas, models, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List, Optional

router = APIRouter(
    prefix="/like",
    tags=['Likes']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def get_posts(like: schemas.LikeBase ,db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == like.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post {like.post_id} does not exist")
    
    like_query = db.query(models.Like).filter(models.Like.post_id == like.post_id, models.Like.user_id == current_user.id)
    found_like = like_query.first()
    if(like.dir == 1):
        if found_like:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} already liked {like.post_id}")
        new_like = models.Like(post_id = like.post_id, user_id = current_user.id)
        db.add(new_like)
        db.commit()
        return {"message": "successfully liked post"}
    else:
        if not found_like:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="like does not exist")
        like_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully unliked post"}


