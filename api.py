# api.py

from fastapi import FastAPI, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Optional
import logging

from src.models.api_models import (
    BookRequest, ManualBookRequest, BookResponse, BooksListResponse,
    DeleteBookResponse, ErrorResponse, HealthResponse, SearchRequest
)
from src.models.book import Book
from src.services.library import Library
from src.utils.exceptions import (
    BookNotFoundError, DuplicateBookError, APIError, InvalidISBNError
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Library Management System",
    description="A modern library management system with Open Library API integration",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize library instance
library = Library()


@app.exception_handler(BookNotFoundError)
async def book_not_found_handler(request, exc):
    """Handle BookNotFoundError exceptions."""
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"error": str(exc)}
    )


@app.exception_handler(DuplicateBookError)
async def duplicate_book_handler(request, exc):
    """Handle DuplicateBookError exceptions."""
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"error": str(exc)}
    )


@app.exception_handler(APIError)
async def api_error_handler(request, exc):
    """Handle APIError exceptions."""
    return JSONResponse(
        status_code=status.HTTP_502_BAD_GATEWAY,
        content={"error": "External API error", "detail": str(exc)}
    )


@app.exception_handler(InvalidISBNError)
async def invalid_isbn_handler(request, exc):
    """Handle InvalidISBNError exceptions."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": str(exc)}
    )


@app.get("/", response_model=dict)
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Library Management System API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": ["/books", "/books/{isbn}", "/search", "/health"]
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    try:
        stats = library.get_statistics()
        return HealthResponse(
            status="healthy",
            library_stats=stats
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service unhealthy"
        )


@app.get("/books", response_model=BooksListResponse)
async def get_books(
    limit: Optional[int] = Query(None, ge=1, le=1000, description="Limit number of books returned"),
    offset: Optional[int] = Query(0, ge=0, description="Offset for pagination")
):
    """Get all books in the library with optional pagination."""
    try:
        books = library.list_books()
        total = len(books)
        
        # Apply pagination if specified
        if limit is not None:
            books = books[offset:offset + limit]
        
        book_responses = [
            BookResponse(
                title=book.title, 
                author=book.author, 
                isbn=book.isbn,
                genre=book.genre
            )
            for book in books
        ]
        
        return BooksListResponse(books=book_responses, total=total)
        
    except Exception as e:
        logger.error(f"Error retrieving books: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve books"
        )


@app.post("/books", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def add_book(book_request: BookRequest):
    """Add a book by ISBN using Open Library API."""
    try:
        book = library.add_book_by_isbn(book_request.isbn)
        logger.info(f"Added book via API: {book}")
        
        return BookResponse(
            title=book.title,
            author=book.author,
            isbn=book.isbn,
            genre=book.genre
        )
        
    except (DuplicateBookError, InvalidISBNError, APIError) as e:
        raise e
    except Exception as e:
        logger.error(f"Unexpected error adding book: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to add book"
        )


@app.post("/books/manual", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def add_book_manual(book_request: ManualBookRequest):
    """Add a book manually without API lookup."""
    try:
        book = library.add_book_manual(
            title=book_request.title,
            author=book_request.author,
            isbn=book_request.isbn,
            genre=book_request.genre
        )
        logger.info(f"Added book manually: {book}")
        
        return BookResponse(
            title=book.title,
            author=book.author,
            isbn=book.isbn,
            genre=book.genre
        )
        
    except DuplicateBookError as e:
        raise e
    except Exception as e:
        logger.error(f"Unexpected error adding book manually: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to add book"
        )


@app.get("/books/{isbn}", response_model=BookResponse)
async def get_book(isbn: str):
    """Get a specific book by ISBN."""
    book = library.find_book(isbn)
    
    if book is None:
        raise BookNotFoundError(f"Book with ISBN {isbn} not found")
    
    return BookResponse(
        title=book.title,
        author=book.author,
        isbn=book.isbn,
        genre=book.genre
    )


@app.delete("/books/{isbn}", response_model=DeleteBookResponse)
async def delete_book(isbn: str):
    """Delete a book by ISBN."""
    book = library.find_book(isbn)
    
    if book is None:
        raise BookNotFoundError(f"Book with ISBN {isbn} not found")
    
    try:
        library.remove_book(isbn)
        logger.info(f"Deleted book: {book}")
        
        return DeleteBookResponse(
            message=f"Book with ISBN {isbn} successfully deleted",
            deleted_book=BookResponse(
                title=book.title,
                author=book.author,
                isbn=book.isbn,
                genre=book.genre
            )
        )
        
    except Exception as e:
        logger.error(f"Error deleting book: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete book"
        )


@app.get("/search", response_model=BooksListResponse)
async def search_books(
    q: str = Query(..., min_length=1, max_length=100, description="Search query"),
    limit: Optional[int] = Query(10, ge=1, le=100, description="Limit search results")
):
    """Search for books by title, author, or ISBN."""
    try:
        books = library.search_books(q)
        
        # Apply limit
        books = books[:limit] if limit else books
        
        book_responses = [
            BookResponse(
                title=book.title, 
                author=book.author, 
                isbn=book.isbn,
                genre=book.genre
            )
            for book in books
        ]
        
        return BooksListResponse(books=book_responses, total=len(book_responses))
        
    except Exception as e:
        logger.error(f"Error searching books: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Search failed"
        )

@app.put("/books/{isbn}", response_model=BookResponse)
async def update_book(isbn: str, updates: dict):
    """Update a book's information."""
    book = library.find_book(isbn)
    
    if book is None:
        raise BookNotFoundError(f"Book with ISBN {isbn} not found")
    
    try:
        # Update book properties
        if 'genre' in updates:
            book.genre = updates['genre']
        if 'title' in updates:
            book.title = updates['title']
        if 'author' in updates:
            book.author = updates['author']
        
        # Save changes
        library.save_books()
        logger.info(f"Updated book: {book}")
        
        return BookResponse(
            title=book.title,
            author=book.author,
            isbn=book.isbn,
            genre=book.genre
        )
        
    except Exception as e:
        logger.error(f"Error updating book: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update book"
        )


@app.get("/stats", response_model=dict)
async def get_library_stats():
    """Get detailed library statistics."""
    try:
        stats = library.get_statistics()
        return {
            "total_books": stats["total_books"],
            "unique_authors": stats["unique_authors"],
            "authors": stats["authors"][:20],
            "total_authors": len(stats["authors"])
        }
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get statistics"
        )


@app.on_event("startup")
async def startup_event():
    """Initialize application on startup."""
    logger.info("Library Management System API starting up...")
    logger.info(f"Loaded {library.get_books_count()} books from storage")


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources on shutdown."""
    logger.info("Library Management System API shutting down...")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
