
# creaiting the model for the database using SQLAlchemy ORM
from sqlalchemy import String, Integer, Column, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from Database import Base
from datetime import datetime
from passlib.context import CryptContext


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    # role = Column(String, default="user")
    # defin the rule::::: for user and admin:::
    is_admin = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    # 1 to many relationship
    blogs = relationship("Blog", back_populates="owner")
    comments = relationship("Comment", back_populates="user")

# creating the blog table in Database ::::
class Blog(Base):
    __tablename__ = "blogs"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    owner = relationship("User", back_populates="blogs")
    comments = relationship("Comment", back_populates="blog")


# creating the table comments ::: in psQL
class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    blog_id = Column(Integer, ForeignKey("blogs.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    # 1 to many relationship
    user = relationship("User", back_populates="comments")
    # 1 to many relationship
    blog = relationship("Blog", back_populates="comments")
