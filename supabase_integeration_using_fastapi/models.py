import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Text, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declarative_base
Base = declarative_base()

class Profile(Base):
    __tablename__ = "profiles"
    id = Column(UUID(as_uuid=True), primary_key=True)  # Supabase user ID (auth.users.id)
    name = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
#    creating the relationship between  
    borrow_records = relationship("BorrowRecord", back_populates="profile", cascade="all, delete-orphan")

class Author(Base):
    __tablename__ = "authors"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    books = relationship("Book", back_populates="author", cascade="all, delete-orphan")

class Category(Base):
    __tablename__ = "categories"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, unique=True)
    books = relationship("Book", back_populates="category", cascade="all, delete-orphan")

class Book(Base):
    __tablename__ = "books"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    isbn = Column(String, unique=True, nullable=False)
    author_id = Column(UUID(as_uuid=True), ForeignKey("authors.id", ondelete="SET NULL"))
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id", ondelete="SET NULL"))
    total_copies = Column(Integer, default=1)
    available_copies = Column(Integer, default=1)
    author = relationship("Author", back_populates="books")
    category = relationship("Category", back_populates="books")
    borrow_records = relationship("BorrowRecord", back_populates="book", cascade="all, delete-orphan")


class BorrowRecord(Base):
    __tablename__ = "borrow_records"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    profile_id = Column(UUID(as_uuid=True), ForeignKey("profiles.id", ondelete="CASCADE"))
    book_id = Column(UUID(as_uuid=True), ForeignKey("books.id", ondelete="CASCADE"))
    borrow_date = Column(DateTime, default=datetime.utcnow)
    return_date = Column(DateTime, nullable=True)
    returned = Column(Boolean, default=False)
    profile = relationship("Profile", back_populates="borrow_records")
    book = relationship("Book", back_populates="borrow_records")
