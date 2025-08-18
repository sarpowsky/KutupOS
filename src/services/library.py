# src/services/library.py

import json
import logging
from pathlib import Path
from typing import List, Optional, Dict, Any
from src.models.book import Book
from src.services.api_service import OpenLibraryService
from src.utils.exceptions import BookNotFoundError, DuplicateBookError, APIError, InvalidISBNError

logger = logging.getLogger(__name__)


class Library:
    """
    Manages a collection of books with persistent storage.
    """
    
    def __init__(self, filename: str = "data/library.json") -> None:
        """Initialize the library with a storage file."""
        self.filename = Path(filename)
        self.books: List[Book] = []
        
        # Create the data directory if it doesn't exist
        self.filename.parent.mkdir(parents=True, exist_ok=True)
        
        # Load existing books when library is created
        self.load_books()
        
        logger.info(f"Library initialized with {len(self.books)} books from {filename}")
    
    def __enter__(self) -> 'Library':
        """Context manager entry - returns the library instance."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit - automatically saves books when leaving context."""
        self.save_books()
        logger.info("Library context closed, books saved automatically")
    
    def add_book(self, book: Book) -> None:
        """Add a new book to the library."""
        if not isinstance(book, Book):
            raise TypeError("Only Book instances can be added to the library")
        
        # Check if book already exists (based on ISBN)
        if self.find_book(book.isbn) is not None:
            raise DuplicateBookError(f"Book with ISBN {book.isbn} already exists in library")
        
        # Add the book and save to file
        self.books.append(book)
        self.save_books()
        
        logger.info(f"Added book: {book}")
    
    def add_book_by_isbn(self, isbn: str) -> Book:
        """Add a book to the library by fetching data from Open Library API."""
        # Check if book already exists
        if self.find_book(isbn) is not None:
            raise DuplicateBookError(f"Book with ISBN {isbn} already exists in library")
        
        try:
            # Fetch book data from API
            api_service = OpenLibraryService()
            book_data = api_service.fetch_book_sync(isbn)
            
            # Create Book instance from API data
            book = Book(
                title=book_data["title"],
                author=book_data["author"],
                isbn=isbn,
                genre=None  # Will be auto-detected by frontend
            )
            
            # Add to library
            self.books.append(book)
            self.save_books()
            
            logger.info(f"Added book from API: {book}")
            return book
            
        except (APIError, InvalidISBNError) as e:
            logger.error(f"Failed to add book by ISBN {isbn}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error adding book by ISBN {isbn}: {e}")
            raise APIError(f"Failed to add book: {e}")
    
    def add_book_manual(self, title: str, author: str, isbn: str, genre: str = None) -> Book:
        """Add a book manually without API lookup."""
        book = Book(title=title, author=author, isbn=isbn, genre=genre)
        self.add_book(book)
        return book
    
    def remove_book(self, isbn: str) -> bool:
        """Remove a book from the library by ISBN."""
        book_to_remove = self.find_book(isbn)
        
        if book_to_remove is None:
            raise BookNotFoundError(f"No book found with ISBN: {isbn}")
        
        # Remove the book and save changes
        self.books.remove(book_to_remove)
        self.save_books()
        
        logger.info(f"Removed book: {book_to_remove}")
        return True
    
    def find_book(self, isbn: str) -> Optional[Book]:
        """Find a book by its ISBN."""
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None
    
    def list_books(self) -> List[Book]:
        """Get all books in the library."""
        return self.books.copy()
    
    def search_books(self, query: str) -> List[Book]:
        """Search for books by title, author, or ISBN."""
        query_lower = query.lower()
        matching_books = []
        
        for book in self.books:
            if (query_lower in book.title.lower() or 
                query_lower in book.author.lower() or 
                query_lower in book.isbn.lower()):
                matching_books.append(book)
        
        return matching_books
    
    def get_books_count(self) -> int:
        """Get the total number of books in the library."""
        return len(self.books)
    
    def load_books(self) -> None:
        """Load books from the JSON storage file."""
        try:
            if self.filename.exists():
                with open(self.filename, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    
                    # Convert dictionary data back to Book objects
                    self.books = [Book.from_dict(book_data) for book_data in data]
                    
                logger.info(f"Loaded {len(self.books)} books from {self.filename}")
            else:
                self.books = []
                logger.info(f"No existing library file found at {self.filename}, starting fresh")
                
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            logger.error(f"Error loading books from {self.filename}: {e}")
            logger.info("Starting with empty library due to file corruption")
            self.books = []
        
        except Exception as e:
            logger.error(f"Unexpected error loading books: {e}")
            self.books = []
    
    def save_books(self) -> None:
        """Save all books to the JSON storage file."""
        try:
            # Create backup of existing file if it exists
            if self.filename.exists():
                backup_path = self.filename.with_suffix('.json.backup')
                self.filename.replace(backup_path)
                logger.debug(f"Created backup at {backup_path}")
            
            # Convert books to dictionary format and save
            books_data = [book.to_dict() for book in self.books]
            
            with open(self.filename, 'w', encoding='utf-8') as file:
                json.dump(books_data, file, indent=2, ensure_ascii=False)
            
            logger.info(f"Saved {len(self.books)} books to {self.filename}")
            
        except Exception as e:
            logger.error(f"Error saving books to {self.filename}: {e}")
            raise
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get library statistics for reporting purposes."""
        if not self.books:
            return {
                "total_books": 0,
                "unique_authors": 0,
                "authors": []
            }
        
        # Count unique authors
        authors = set(book.author for book in self.books)
        
        return {
            "total_books": len(self.books),
            "unique_authors": len(authors),
            "authors": sorted(list(authors))
        }
    
    def clear_library(self) -> None:
        """Remove all books from the library."""
        book_count = len(self.books)
        self.books.clear()
        self.save_books()
        
        logger.warning(f"Cleared library - removed {book_count} books")