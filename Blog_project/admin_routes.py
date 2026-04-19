from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from model import User, Blog, Comment
from dependencies import require_admin
from Database import get_db
from auth import hash_password 
from pydantic import BaseModel , EmailStr
# setting up the Adminn Routesss :::
router = APIRouter(prefix="/admin", tags=["Admin Routes"])

@router.get("/profile")
def get_admin_profile(current_admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    return {
        "admin_id": current_admin.id,
        "username": current_admin.username,
        "email": current_admin.email,
        "role": "Admin",
        "created_at": current_admin.created_at
    }

# Creating or adding any user in the Database ::::
class AdminCreateUser(BaseModel):
    username: str
    email: EmailStr
    password: str
    is_admin: bool = False  

@router.post("/create_user")
def create_user(new_user: AdminCreateUser , db:Session =Depends(get_db),current_admin=Depends(require_admin)):
    #check if the user already exist or not :: in the Database :::
        existing_user = db.query(User).filter(
        (User.username == new_user.username) | (User.email == new_user.email)
    ).first()
        if existing_user:
             raise HTTPException(status_code=400, detail="Username or email already exists")
        # Create user
        user = User(
        username=new_user.username,
        email=new_user.email,
        password=hash_password(new_user.password),
        is_admin=new_user.is_admin
    )
        db.add(user)
        db.commit()
        db.refresh(user)
    
        return {
        "message": "User created successfully",
        "user_id": user.id,
        "role": "Admin" if user.is_admin else "User"
    }

# Adding the Remove user Functionality :::
@router.delete("/delete-user/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), current_admin = Depends(require_admin)):
    # Query the database for the user by their id
    user_to_delete = db.query(User).filter(User.id == user_id).first()
    if not user_to_delete:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user_to_delete)
    db.commit()
    return {"message": f"User '{user_to_delete.username}' deleted successfully"}

#   Admin can also view all blogs In the Database 
@router.get("/view-all-blogs")
def view_all_blogs(db: Session = Depends(get_db), current_admin = Depends(require_admin)):
    blogs = db.query(Blog).all()
    all_blogs = []
    for blog in blogs:
        author = db.query(User).filter(User.id == blog.author_id).first()
        all_blogs.append({
            "id": blog.id,
            "title": blog.title,
            "content": blog.content,
            "author": author.username if author else "Unknown",
            "created_at": blog.created_at
        })
    return {"all_blogs": all_blogs}
# adding the Remove blog by ID::
@router.delete("/remove-blog/{blog_id}")
def delete_blog(blog_id: int, db: Session=Depends(get_db),current_admin=Depends(require_admin)):
     blog_to_delete=db.query(Blog).filter(Blog.id==blog_id).first()
     if not blog_to_delete:
          raise HTTPException (status_code= 404 , detail="blog not Found")
     db.delete(blog_to_delete)
     db.commit()
     return{"Blog Deteled from the Database Sucessfully"}
     
# Removing any comment from the blog ( in comment table)::
@router.delete("remove-comment/{comment_id}")
def remove_any_comment(comment_id : int, db :Session=Depends(get_db),Current_admin=Depends(require_admin)):
     comment_to_remove=db.query(Comment).filter(Comment.id==comment_id).first()
     if not comment_id:
          raise HTTPException(status_code=404,detail="Comments not Found")     
     else:
          db.delete(comment_to_remove)
          db.commit()
          db.refresh()
          return{
               "Comment Has been Successfullly removed!"
          }
# Admin can view all users ::
@router.get("/view-all-users")
def get_all_users(db: Session = Depends(get_db), current_admin = Depends(require_admin)):
    users = db.query(User).all()
    all_users = []
    for user in users:
        all_users.append({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_admin": user.is_admin,
            "created_at": user.created_at
        })
    return {"users": all_users}

# admin can view all comments::
@router.get("/view-all-comments")
def view_comments(db: Session = Depends(get_db), current_admin = Depends(require_admin)):
    all_comments = db.query(Comment).all()
    comments = []
    for comment in all_comments:
        blog = db.query(Blog).filter(Blog.id == comment.blog_id).first()
        user = db.query(User).filter(User.id == comment.user_id).first()
        comments.append({
            "comment_id": comment.id,
            "content": comment.content,
            "blog_title": blog.title if blog else "Unknown",
            "by_user": user.username if user else "Unknown",
            "created_at": comment.created_at
        })
    return {"comments": comments}

