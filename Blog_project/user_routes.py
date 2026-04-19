from fastapi import APIRouter, Depends ,HTTPException
from sqlalchemy.orm import Session
from Database import get_db
from dependencies import require_user
from pydantic import BaseModel
from model import Blog #importing the Blog class from the model.py file contains Schema for Database
from datetime import datetime
from typing import Optional
from model import User, Comment
# //setting up the user routes for the usersss amd using dependcies to verify the authorization First:::
router = APIRouter(prefix="/user", tags=["user Routes"])
@router.get("/profile")
def get_user_profile(current_user=Depends(require_user)):    
    return {
        "username": current_user.username,
        "email": current_user.email,
        "role": "Admin" if current_user.is_admin else "User"
    }
# Pydantic schema for creating blog
class CreateBlog(BaseModel):
    title: str
    content: str
# creatin a Pydantic model for updating the blog by author::
class UpdateBlog(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

# Route to create blog
@router.post("/blog")
def create_blog(blog: CreateBlog, db: Session = Depends(get_db), current_user=Depends(require_user)):
    new_blog = Blog(
        title=blog.title,
        content=blog.content,
        author_id=current_user.id,
        created_at=datetime.utcnow()
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return {
        "message": "Blog created successfully",
        "blog_id": new_blog.id,
        "author": current_user.username
    }

# update blog by blog_id::::
@router.put("/blog/{blog_id}")
def update_blog(blog_id: int, update_data: UpdateBlog, db: Session = Depends(get_db), current_user=Depends(require_user)):
    # checking if blog id exist or not ::::::
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not blog:
        return{"Blog does not exist in the Database"}
    # checkin the ownership of the Blog:: with author_id and blog_id matched or not 
    if blog.author_id !=current_user.id:
        return{"you can not edit this blog "}
    if update_data.title:
        blog.title = update_data.title
    if update_data.content:
        blog.content = update_data.content
    blog.created_at = datetime.utcnow()
    db.commit()
    db.refresh(blog)
    return {
        "message": "Blog updated successfully",
        "blog_id": blog.id,
        "updated_title": blog.title,
        "updated_content": blog.content
    }
# view all blogs Functions::::
@router.get("/all_blogs")
def view_all_blogs(db: Session = Depends(get_db), current_user = Depends(require_user)):
    blogs = db.query(Blog).all()
    result = []
    for blog in blogs:
        result.append({
            "id": blog.id,
            "title": blog.title,
            "content": blog.content,
            # "author": db.query(User).filter(User.id == blog.author_id).first().username,
            "created_at": blog.created_at
        })
    return result   

#Adding comments on the blog :::
class CreateComment(BaseModel):
    blog_id: int
    content: str
@router.post("/comment")
def add_comment(comment: CreateComment, db: Session = Depends(get_db), current_user = Depends(require_user)):
    blog = db.query(Blog).filter(Blog.id == comment.blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    new_comment = Comment(
        content=comment.content,
        user_id=current_user.id,
        blog_id=comment.blog_id,
        created_at=datetime.utcnow()
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return {
        "message": "Comment added successfully",
        "comment_id": new_comment.id,
        "blog_title": blog.title,
        "by_user": current_user.username
    }
