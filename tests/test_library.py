# tests/test_library.py

import pytest
import json
import tempfile
from pathlib import Path
from unittest.mock import patch, mock_open
import sys
import os

# Add the parent directory to sys.path to enable imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.models.book import Book
from src.services.library import Library
from src.utils.exceptions import BookNotFoundError, DuplicateBookError


class TestLibrary:
    """
    Test suite for the Library class.
    
    These tests cover all library operations including persistence,
    error handling, and edge cases.
    """
    
    @pytest.fixture
    def temp_library_file(self):
        """Create a temporary file for testing library persistence."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_path = f.name
        yield temp_path
        # Cleanup
        Path(temp_path).unlink(missing_ok=True)
    
    @pytest.fixture
    def sample_book(self):
        """Sample book for testing."""
        return Book("Test Book", "Test Author", "123456789")
    
    @pytest.fixture
    def sample_books(self):
        """List of sample books for testing."""
        return [
            Book("Book One", "Author A", "111111111"),
            Book("Book Two", "Author B", "222222222"),
            Book("Book Three", "Author A", "333333333")
        ]
    
    def test_library_initialization_with_default_filename(self):
        """Test library initializes with default filename."""
        with patch('src.services.library.Library.load_books'):
            library = Library()
            assert library.filename == Path("data/library.json")
    
    def test_library_initialization_with_custom_filename(self, temp_library_file):
        """Test library initializes with custom filename."""
        library = Library(temp_library_file)
        assert library.filename == Path(temp_library_file)
    
    def test_library_initialization_creates_directory(self):
        """Test library creates data directory if it doesn't exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = Path(temp_dir) / "subdir" / "library.json"
            library = Library(str(test_file))
            assert test_file.parent.exists()
    
    def test_add_book_success(self, temp_library_file, sample_book):
        """Test successfully adding a book to the library."""
        library = Library(temp_library_file)
        
        library.add_book(sample_book)
        
        assert len(library.books) == 1
        assert library.books[0] == sample_book
    
    def test_add_book_invalid_type_raises_error(self, temp_library_file):
        """Test adding non-Book object raises TypeError."""
        library = Library(temp_library_file)
        
        with pytest.raises(TypeError, match="Only Book instances can be added"):
            library.add_book("not a book")
    
    def test_add_duplicate_book_raises_error(self, temp_library_file, sample_book):
        """Test adding duplicate book raises DuplicateBookError."""
        library = Library(temp_library_file)
        library.add_book(sample_book)
        
        duplicate_book = Book("Different Title", "Different Author", sample_book.isbn)
        
        with pytest.raises(DuplicateBookError, match="already exists"):
            library.add_book(duplicate_book)
    
    def test_remove_book_success(self, temp_library_file, sample_book):
        """Test successfully removing a book."""
        library = Library(temp_library_file)
        library.add_book(sample_book)
        
        result = library.remove_book(sample_book.isbn)
        
        assert result == True
        assert len(library.books) == 0
    
    def test_remove_nonexistent_book_raises_error(self, temp_library_file):
        """Test removing non-existent book raises BookNotFoundError."""
        library = Library(temp_library_file)
        
        with pytest.raises(BookNotFoundError, match="No book found"):
            library.remove_book("nonexistent-isbn")
    
    def test_find_book_success(self, temp_library_file, sample_books):
        """Test successfully finding a book by ISBN."""
        library = Library(temp_library_file)
        for book in sample_books:
            library.add_book(book)
        
        found_book = library.find_book("222222222")
        
        assert found_book is not None
        assert found_book.title == "Book Two"
        assert found_book.isbn == "222222222"
    
    def test_find_book_not_found(self, temp_library_file, sample_books):
        """Test finding non-existent book returns None."""
        library = Library(temp_library_file)
        for book in sample_books:
            library.add_book(book)
        
        found_book = library.find_book("nonexistent")
        
        assert found_book is None
    
    def test_list_books_returns_copy(self, temp_library_file, sample_books):
        """Test list_books returns a copy to prevent external modification."""
        library = Library(temp_library_file)
        for book in sample_books:
            library.add_book(book)
        
        books_list = library.list_books()
        books_list.clear()  # Modify the returned list
        
        # Original library should still have books
        assert len(library.books) == 3
        assert len(library.list_books()) == 3
    
    def test_search_books_by_title(self, temp_library_file, sample_books):
        """Test searching books by title."""
        library = Library(temp_library_file)
        for book in sample_books:
            library.add_book(book)
        
        results = library.search_books("Book Two")
        
        assert len(results) == 1
        assert results[0].title == "Book Two"
    
    def test_search_books_by_author(self, temp_library_file, sample_books):
        """Test searching books by author."""
        library = Library(temp_library_file)
        for book in sample_books:
            library.add_book(book)
        
        results = library.search_books("Author A")
        
        assert len(results) == 2  # Two books by Author A
        assert all("Author A" in book.author for book in results)
    
    def test_search_books_case_insensitive(self, temp_library_file, sample_books):
        """Test search is case insensitive."""
        library = Library(temp_library_file)
        for book in sample_books:
            library.add_book(book)
        
        results = library.search_books("book one")  # lowercase
        
        assert len(results) == 1
        assert results[0].title == "Book One"
    
    def test_search_books_no_results(self, temp_library_file, sample_books):
        """Test search with no matching results."""
        library = Library(temp_library_file)
        for book in sample_books:
            library.add_book(book)
        
        results = library.search_books("Nonexistent")
        
        assert len(results) == 0
    
    def test_get_books_count(self, temp_library_file, sample_books):
        """Test getting total count of books."""
        library = Library(temp_library_file)
        
        assert library.get_books_count() == 0
        
        for book in sample_books:
            library.add_book(book)
        
        assert library.get_books_count() == 3
    
    def test_clear_library(self, temp_library_file, sample_books):
        """Test clearing all books from library."""
        library = Library(temp_library_file)
        for book in sample_books:
            library.add_book(book)
        
        library.clear_library()
        
        assert len(library.books) == 0
        assert library.get_books_count() == 0
    
    def test_get_statistics_empty_library(self, temp_library_file):
        """Test statistics for empty library."""
        library = Library(temp_library_file)
        
        stats = library.get_statistics()
        
        assert stats["total_books"] == 0
        assert stats["unique_authors"] == 0
        assert stats["authors"] == []
    
    def test_get_statistics_with_books(self, temp_library_file, sample_books):
        """Test statistics with books in library."""
        library = Library(temp_library_file)
        for book in sample_books:
            library.add_book(book)
        
        stats = library.get_statistics()
        
        assert stats["total_books"] == 3
        assert stats["unique_authors"] == 2  # Author A and Author B
        assert "Author A" in stats["authors"]
        assert "Author B" in stats["authors"]
    
    def test_save_books_creates_valid_json(self, temp_library_file, sample_books):
        """Test saving books creates valid JSON file."""
        library = Library(temp_library_file)
        for book in sample_books:
            library.add_book(book)
        
        library.save_books()
        
        # Verify file exists and contains valid JSON
        assert Path(temp_library_file).exists()
        
        with open(temp_library_file, 'r') as f:
            data = json.load(f)
        
        assert len(data) == 3
        assert all(isinstance(book_data, dict) for book_data in data)
        assert all(set(book_data.keys()) == {"title", "author", "isbn"} for book_data in data)
    
    def test_load_books_from_valid_json(self, temp_library_file):
        """Test loading books from valid JSON file."""
        # Create test data
        test_data = [
            {"title": "Test Book 1", "author": "Test Author 1", "isbn": "111"},
            {"title": "Test Book 2", "author": "Test Author 2", "isbn": "222"}
        ]
        
        with open(temp_library_file, 'w') as f:
            json.dump(test_data, f)
        
        library = Library(temp_library_file)
        
        assert len(library.books) == 2
        assert library.books[0].title == "Test Book 1"
        assert library.books[1].title == "Test Book 2"
    
    def test_load_books_nonexistent_file(self, temp_library_file):
        """Test loading from non-existent file starts with empty library."""
        # Use a file that doesn't exist
        nonexistent_file = temp_library_file + "_nonexistent"
        
        library = Library(nonexistent_file)
        
        assert len(library.books) == 0
    
    def test_load_books_corrupted_json(self, temp_library_file):
        """Test loading from corrupted JSON file starts with empty library."""
        # Write invalid JSON
        with open(temp_library_file, 'w') as f:
            f.write("invalid json content")
        
        library = Library(temp_library_file)
        
        assert len(library.books) == 0
    
    def test_load_books_invalid_book_data(self, temp_library_file):
        """Test loading from file with invalid book data starts with empty library."""
        # Write JSON with missing required fields
        test_data = [
            {"title": "Test Book", "author": "Test Author"},  # Missing ISBN
        ]
        
        with open(temp_library_file, 'w') as f:
            json.dump(test_data, f)
        
        library = Library(temp_library_file)
        
        assert len(library.books) == 0
    
    def test_context_manager_saves_on_exit(self, temp_library_file, sample_book):
        """Test context manager automatically saves books on exit."""
        with Library(temp_library_file) as library:
            library.add_book(sample_book)
        
        # Verify data was saved by creating new library instance
        new_library = Library(temp_library_file)
        assert len(new_library.books) == 1
        assert new_library.books[0].title == sample_book.title
    
    def test_context_manager_saves_on_exception(self, temp_library_file, sample_book):
        """Test context manager saves books even when exception occurs."""
        try:
            with Library(temp_library_file) as library:
                library.add_book(sample_book)
                raise ValueError("Test exception")
        except ValueError:
            pass
        
        # Verify data was saved despite exception
        new_library = Library(temp_library_file)
        assert len(new_library.books) == 1
    
    def test_save_books_creates_backup(self, temp_library_file, sample_book):
        """Test that save_books creates backup of existing file."""
        library = Library(temp_library_file)
        library.add_book(sample_book)
        library.save_books()  # First save
        
        # Add another book and save again
        another_book = Book("Another Book", "Another Author", "999999999")
        library.add_book(another_book)
        library.save_books()  # Second save should create backup
        
        backup_file = Path(temp_library_file).with_suffix('.json.backup')
        assert backup_file.exists()
    
    @patch('src.services.library.logger')
    def test_logging_on_operations(self, mock_logger, temp_library_file, sample_book):
        """Test that library operations are properly logged."""
        library = Library(temp_library_file)
        
        library.add_book(sample_book)
        mock_logger.info.assert_called()
        
        library.remove_book(sample_book.isbn)
        mock_logger.info.assert_called()
        
        library.clear_library()
        mock_logger.warning.assert_called()


class TestLibraryIntegration:
    """Integration tests for the Library class with real file operations."""
    
    def test_full_library_workflow(self):
        """Test complete library workflow with real file operations."""
        with tempfile.TemporaryDirectory() as temp_dir:
            library_file = Path(temp_dir) / "test_library.json"
            
            # Create library and add books
            with Library(str(library_file)) as library:
                book1 = Book("Book 1", "Author 1", "111")
                book2 = Book("Book 2", "Author 2", "222")
                
                library.add_book(book1)
                library.add_book(book2)
                
                # Test operations
                assert library.get_books_count() == 2
                found_book = library.find_book("111")
                assert found_book.title == "Book 1"
                
                # Remove a book
                library.remove_book("222")
                assert library.get_books_count() == 1
            
            # Verify persistence by creating new library instance
            new_library = Library(str(library_file))
            assert new_library.get_books_count() == 1
            assert new_library.find_book("111") is not None
            assert new_library.find_book("222") is None