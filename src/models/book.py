# src/models/book.py

from typing import Optional


class Book:
    """Represents a book in our library management system."""
    
    def __init__(self, title: str, author: str, isbn: str, genre: Optional[str] = None) -> None:
        """Initialize a new Book instance."""
        if not title.strip():
            raise ValueError("Book title cannot be empty")
        if not author.strip():
            raise ValueError("Book author cannot be empty")
        if not isbn.strip():
            raise ValueError("Book ISBN cannot be empty")
            
        self.title = title.strip()
        self.author = author.strip()
        self.isbn = isbn.strip()
        self.genre = genre.strip() if genre else None
    
    def __str__(self) -> str:
        """Return a human-readable string representation of the book."""
        return f"{self.title} by {self.author} (ISBN: {self.isbn})"
    
    def __repr__(self) -> str:
        """Return a developer-friendly representation of the book."""
        return f"Book(title='{self.title}', author='{self.author}', isbn='{self.isbn}', genre='{self.genre}')"
    
    def __eq__(self, other) -> bool:
        """Check if two books are equal based on their ISBN."""
        if not isinstance(other, Book):
            return False
        return self.isbn == other.isbn
    
    def __hash__(self) -> int:
        """Generate a hash value for the book based on ISBN."""
        return hash(self.isbn)
    
    def to_dict(self) -> dict:
        """Convert the book to a dictionary for JSON serialization."""
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "genre": self.genre
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Book':
        """Create a Book instance from a dictionary."""
        try:
            return cls(
                title=data["title"],
                author=data["author"], 
                isbn=data["isbn"],
                genre=data.get("genre")
            )
        except KeyError as e:
            raise KeyError(f"Missing required field in book data: {e}")
    
    def is_valid_isbn(self) -> bool:
        """Perform basic ISBN validation."""
        clean_isbn = self.isbn.replace("-", "").replace(" ", "")
        
        if len(clean_isbn) == 10:
            return clean_isbn[:9].isdigit()
        elif len(clean_isbn) == 13:
            return clean_isbn.isdigit()
        
        return False