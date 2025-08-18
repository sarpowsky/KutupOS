# tests/test_book.py

import pytest
import sys
import os

# Add the parent directory to sys.path to enable imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.models.book import Book


class TestBook:
    """
    Test suite for the Book class.
    
    These tests ensure that our Book class behaves correctly
    in all scenarios including edge cases and error conditions.
    """
    
    def test_book_creation_valid_data(self):
        """Test creating a book with valid data."""
        book = Book("The Great Gatsby", "F. Scott Fitzgerald", "978-0-7432-7356-5")
        
        assert book.title == "The Great Gatsby"
        assert book.author == "F. Scott Fitzgerald"
        assert book.isbn == "978-0-7432-7356-5"
    
    def test_book_creation_strips_whitespace(self):
        """Test that book creation strips leading/trailing whitespace."""
        book = Book("  Title  ", "  Author  ", "  ISBN  ")
        
        assert book.title == "Title"
        assert book.author == "Author"
        assert book.isbn == "ISBN"
    
    def test_book_creation_empty_title_raises_error(self):
        """Test that empty title raises ValueError."""
        with pytest.raises(ValueError, match="Book title cannot be empty"):
            Book("", "Author", "ISBN")
    
    def test_book_creation_empty_author_raises_error(self):
        """Test that empty author raises ValueError."""
        with pytest.raises(ValueError, match="Book author cannot be empty"):
            Book("Title", "", "ISBN")
    
    def test_book_creation_empty_isbn_raises_error(self):
        """Test that empty ISBN raises ValueError."""
        with pytest.raises(ValueError, match="Book ISBN cannot be empty"):
            Book("Title", "Author", "")
    
    def test_book_creation_whitespace_only_fields_raise_error(self):
        """Test that fields with only whitespace raise ValueError."""
        with pytest.raises(ValueError):
            Book("   ", "Author", "ISBN")
        
        with pytest.raises(ValueError):
            Book("Title", "   ", "ISBN")
        
        with pytest.raises(ValueError):
            Book("Title", "Author", "   ")
    
    def test_str_representation(self):
        """Test the string representation of a book."""
        book = Book("1984", "George Orwell", "978-0-452-28423-4")
        expected = "1984 by George Orwell (ISBN: 978-0-452-28423-4)"
        
        assert str(book) == expected
    
    def test_repr_representation(self):
        """Test the repr representation of a book."""
        book = Book("1984", "George Orwell", "978-0-452-28423-4")
        expected = "Book(title='1984', author='George Orwell', isbn='978-0-452-28423-4')"
        
        assert repr(book) == expected
    
    def test_book_equality_same_isbn(self):
        """Test that books with same ISBN are considered equal."""
        book1 = Book("Title1", "Author1", "123456789")
        book2 = Book("Title2", "Author2", "123456789")  # Different title/author, same ISBN
        
        assert book1 == book2
    
    def test_book_equality_different_isbn(self):
        """Test that books with different ISBN are not equal."""
        book1 = Book("Same Title", "Same Author", "123456789")
        book2 = Book("Same Title", "Same Author", "987654321")
        
        assert book1 != book2
    
    def test_book_equality_with_non_book_object(self):
        """Test that book is not equal to non-Book objects."""
        book = Book("Title", "Author", "ISBN")
        
        assert book != "string"
        assert book != 123
        assert book != None
        assert book != {"title": "Title", "author": "Author", "isbn": "ISBN"}
    
    def test_book_hash_same_isbn(self):
        """Test that books with same ISBN have same hash."""
        book1 = Book("Title1", "Author1", "123456789")
        book2 = Book("Title2", "Author2", "123456789")
        
        assert hash(book1) == hash(book2)
    
    def test_book_hash_different_isbn(self):
        """Test that books with different ISBN have different hash."""
        book1 = Book("Title", "Author", "123456789")
        book2 = Book("Title", "Author", "987654321")
        
        assert hash(book1) != hash(book2)
    
    def test_books_can_be_used_in_set(self):
        """Test that books can be stored in a set (requires hash and eq)."""
        book1 = Book("Title1", "Author1", "123456789")
        book2 = Book("Title2", "Author2", "987654321")
        book3 = Book("Title3", "Author3", "123456789")  # Same ISBN as book1
        
        book_set = {book1, book2, book3}
        
        # Should only have 2 books since book1 and book3 have same ISBN
        assert len(book_set) == 2
        assert book1 in book_set
        assert book2 in book_set
    
    def test_to_dict_conversion(self):
        """Test converting book to dictionary."""
        book = Book("The Catcher in the Rye", "J.D. Salinger", "978-0-316-76948-0")
        expected_dict = {
            "title": "The Catcher in the Rye",
            "author": "J.D. Salinger",
            "isbn": "978-0-316-76948-0"
        }
        
        assert book.to_dict() == expected_dict
    
    def test_from_dict_creation(self):
        """Test creating book from dictionary."""
        data = {
            "title": "To Kill a Mockingbird",
            "author": "Harper Lee",
            "isbn": "978-0-06-112008-4"
        }
        
        book = Book.from_dict(data)
        
        assert book.title == "To Kill a Mockingbird"
        assert book.author == "Harper Lee"
        assert book.isbn == "978-0-06-112008-4"
    
    def test_from_dict_missing_title_raises_error(self):
        """Test that missing title in dict raises KeyError."""
        data = {"author": "Author", "isbn": "ISBN"}
        
        with pytest.raises(KeyError, match="Missing required field"):
            Book.from_dict(data)
    
    def test_from_dict_missing_author_raises_error(self):
        """Test that missing author in dict raises KeyError."""
        data = {"title": "Title", "isbn": "ISBN"}
        
        with pytest.raises(KeyError, match="Missing required field"):
            Book.from_dict(data)
    
    def test_from_dict_missing_isbn_raises_error(self):
        """Test that missing ISBN in dict raises KeyError."""
        data = {"title": "Title", "author": "Author"}
        
        with pytest.raises(KeyError, match="Missing required field"):
            Book.from_dict(data)
    
    def test_from_dict_empty_values_raise_error(self):
        """Test that empty values in dict raise ValueError."""
        data = {"title": "", "author": "Author", "isbn": "ISBN"}
        
        with pytest.raises(ValueError):
            Book.from_dict(data)
    
    def test_isbn_validation_isbn10_valid(self):
        """Test ISBN validation for valid ISBN-10 format."""
        book = Book("Title", "Author", "0-452-28423-0")
        assert book.is_valid_isbn() == True
        
        book2 = Book("Title", "Author", "045228423X")  # With X check digit
        assert book2.is_valid_isbn() == True
    
    def test_isbn_validation_isbn13_valid(self):
        """Test ISBN validation for valid ISBN-13 format."""
        book = Book("Title", "Author", "978-0-452-28423-4")
        assert book.is_valid_isbn() == True
        
        book2 = Book("Title", "Author", "9780452284234")  # Without hyphens
        assert book2.is_valid_isbn() == True
    
    def test_isbn_validation_invalid_length(self):
        """Test ISBN validation for invalid length."""
        book = Book("Title", "Author", "123")  # Too short
        assert book.is_valid_isbn() == False
        
        book2 = Book("Title", "Author", "12345678901234")  # Too long
        assert book2.is_valid_isbn() == False
    
    def test_isbn_validation_invalid_characters(self):
        """Test ISBN validation for invalid characters."""
        book = Book("Title", "Author", "abc-def-ghi-j")
        assert book.is_valid_isbn() == False
        
        book2 = Book("Title", "Author", "978-0-452-284a3-4")
        assert book2.is_valid_isbn() == False
    
    def test_round_trip_dict_conversion(self):
        """Test that to_dict -> from_dict preserves book data."""
        original_book = Book("Brave New World", "Aldous Huxley", "978-0-06-085052-4")
        
        # Convert to dict and back
        book_dict = original_book.to_dict()
        restored_book = Book.from_dict(book_dict)
        
        # Should be equal and have same attributes
        assert original_book == restored_book
        assert original_book.title == restored_book.title
        assert original_book.author == restored_book.author
        assert original_book.isbn == restored_book.isbn


# Test fixtures for common book instances
@pytest.fixture
def sample_book():
    """Fixture providing a sample book for testing."""
    return Book("The Lord of the Rings", "J.R.R. Tolkien", "978-0-547-92822-7")


@pytest.fixture
def sample_books_list():
    """Fixture providing a list of sample books for testing."""
    return [
        Book("The Hobbit", "J.R.R. Tolkien", "978-0-547-92822-1"),
        Book("1984", "George Orwell", "978-0-452-28423-4"),
        Book("Pride and Prejudice", "Jane Austen", "978-0-14-143951-8")
    ]