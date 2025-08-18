# src/models/api_models.py

from typing import Optional, List
from pydantic import BaseModel, Field, validator


class BookRequest(BaseModel):
    """Request model for adding a book by ISBN."""
    isbn: str = Field(..., description="ISBN of the book to add", min_length=10, max_length=17)
    
    @validator('isbn')
    def validate_isbn(cls, v):
        """Validate ISBN format - more lenient validation."""
        if not v or not v.strip():
            raise ValueError("ISBN cannot be empty")
        
        clean_isbn = v.replace("-", "").replace(" ", "").strip()
        
        if len(clean_isbn) < 10 or len(clean_isbn) > 13:
            raise ValueError("ISBN must be between 10-13 characters")
        
        if not clean_isbn.replace("X", "").replace("x", "").isdigit():
            raise ValueError("ISBN must contain only digits and optionally 'X'")
        
        return v.strip()


class ManualBookRequest(BaseModel):
    """Request model for manually adding a book."""
    title: str = Field(..., description="Book title", min_length=1, max_length=500)
    author: str = Field(..., description="Book author", min_length=1, max_length=200)
    isbn: str = Field(..., description="Book ISBN", min_length=10, max_length=17)
    genre: Optional[str] = Field(None, description="Book genre", max_length=100)
    
    @validator('title', 'author', 'isbn')
    def validate_not_empty(cls, v):
        """Ensure fields are not empty or just whitespace."""
        if not v or not v.strip():
            raise ValueError("Field cannot be empty")
        return v.strip()
    
    @validator('genre')
    def validate_genre(cls, v):
        """Validate genre if provided."""
        if v:
            return v.strip()
        return v


class BookResponse(BaseModel):
    """Response model for book data."""
    title: str = Field(..., description="Book title")
    author: str = Field(..., description="Book author")
    isbn: str = Field(..., description="Book ISBN")
    genre: Optional[str] = Field(None, description="Book genre")
    
    class Config:
        from_attributes = True


class BooksListResponse(BaseModel):
    """Response model for list of books."""
    books: List[BookResponse] = Field(..., description="List of books")
    total: int = Field(..., description="Total number of books")


class DeleteBookResponse(BaseModel):
    """Response model for book deletion."""
    message: str = Field(..., description="Deletion confirmation message")
    deleted_book: BookResponse = Field(..., description="Details of deleted book")


class ErrorResponse(BaseModel):
    """Response model for errors."""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Additional error details")


class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str = Field(..., description="Service status")
    library_stats: dict = Field(..., description="Library statistics")


class SearchRequest(BaseModel):
    """Request model for book search."""
    query: str = Field(..., description="Search query", min_length=1, max_length=100)
    
    @validator('query')
    def validate_query(cls, v):
        """Validate search query."""
        if not v.strip():
            raise ValueError("Search query cannot be empty")
        return v.strip()