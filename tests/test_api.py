# tests/test_api.py

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
import tempfile
import json
import sys
import os

# Add the parent directory to sys.path to enable imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from api import app
from src.models.book import Book
from src.services.library import Library


class TestLibraryAPI:
    """Test suite for the FastAPI application."""
    
    @pytest.fixture
    def client(self):
        """Create test client."""
        return TestClient(app)
    
    @pytest.fixture(autouse=True)
    def setup_test_library(self):
        """Set up clean library for each test."""
        with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as f:
            test_file = f.name
        
        with patch('api.library') as mock_library:
            mock_library.filename = test_file
            mock_library.list_books.return_value = []
            mock_library.get_books_count.return_value = 0
            mock_library.get_statistics.return_value = {
                "total_books": 0,
                "unique_authors": 0,
                "authors": []
            }
            yield mock_library
    
    def test_root_endpoint(self, client):
        """Test root endpoint returns API information."""
        response = client.get("/")
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "endpoints" in data
    
    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "healthy"
        assert "library_stats" in data
    
    def test_get_books_empty_library(self, client):
        """Test getting books from empty library."""
        response = client.get("/books")
        assert response.status_code == 200
        
        data = response.json()
        assert data["books"] == []
        assert data["total"] == 0
    
    @patch('api.library')
    def test_get_books_with_data(self, mock_library, client):
        """Test getting books with data."""
        test_books = [
            Book("Test Book 1", "Author 1", "123"),
            Book("Test Book 2", "Author 2", "456")
        ]
        mock_library.list_books.return_value = test_books
        
        response = client.get("/books")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["books"]) == 2
        assert data["total"] == 2
        assert data["books"][0]["title"] == "Test Book 1"
    
    def test_get_books_with_pagination(self, client):
        """Test book listing with pagination."""
        response = client.get("/books?limit=5&offset=0")
        assert response.status_code == 200
    
    @patch('api.library')
    def test_add_book_success(self, mock_library, client):
        """Test successfully adding a book via API."""
        test_book = Book("Test Title", "Test Author", "1234567890")
        mock_library.add_book_by_isbn.return_value = test_book
        
        response = client.post("/books", json={"isbn": "1234567890"})
        assert response.status_code == 201
        
        data = response.json()
        assert data["title"] == "Test Title"
        assert data["author"] == "Test Author"
        assert data["isbn"] == "1234567890"
    
    def test_add_book_invalid_isbn(self, client):
        """Test adding book with invalid ISBN."""
        response = client.post("/books", json={"isbn": "invalid"})
        assert response.status_code == 422  # Validation error
    
    @patch('api.library')
    def test_add_book_manual_success(self, mock_library, client):
        """Test manually adding a book."""
        test_book = Book("Manual Book", "Manual Author", "9876543210")
        mock_library.add_book_manual.return_value = test_book
        
        response = client.post("/books/manual", json={
            "title": "Manual Book",
            "author": "Manual Author",
            "isbn": "9876543210"
        })
        assert response.status_code == 201
        
        data = response.json()
        assert data["title"] == "Manual Book"
    
    def test_add_book_manual_invalid_data(self, client):
        """Test manual book addition with invalid data."""
        response = client.post("/books/manual", json={
            "title": "",
            "author": "Author",
            "isbn": "123"
        })
        assert response.status_code == 422
    
    @patch('api.library')
    def test_get_book_by_isbn_found(self, mock_library, client):
        """Test getting specific book by ISBN."""
        test_book = Book("Found Book", "Found Author", "1111111111")
        mock_library.find_book.return_value = test_book
        
        response = client.get("/books/1111111111")
        assert response.status_code == 200
        
        data = response.json()
        assert data["title"] == "Found Book"
        assert data["isbn"] == "1111111111"
    
    @patch('api.library')
    def test_get_book_by_isbn_not_found(self, mock_library, client):
        """Test getting non-existent book."""
        mock_library.find_book.return_value = None
        
        response = client.get("/books/nonexistent")
        assert response.status_code == 404
        
        data = response.json()
        assert "error" in data
    
    @patch('api.library')
    def test_delete_book_success(self, mock_library, client):
        """Test successfully deleting a book."""
        test_book = Book("Delete Me", "Delete Author", "2222222222")
        mock_library.find_book.return_value = test_book
        mock_library.remove_book.return_value = True
        
        response = client.delete("/books/2222222222")
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert data["deleted_book"]["title"] == "Delete Me"
    
    @patch('api.library')
    def test_delete_book_not_found(self, mock_library, client):
        """Test deleting non-existent book."""
        mock_library.find_book.return_value = None
        
        response = client.delete("/books/nonexistent")
        assert response.status_code == 404
    
    @patch('api.library')
    def test_search_books(self, mock_library, client):
        """Test book search functionality."""
        test_books = [Book("Search Result", "Search Author", "3333333333")]
        mock_library.search_books.return_value = test_books
        
        response = client.get("/search?q=search")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["books"]) == 1
        assert data["books"][0]["title"] == "Search Result"
    
    def test_search_books_empty_query(self, client):
        """Test search with empty query."""
        response = client.get("/search?q=")
        assert response.status_code == 422
    
    @patch('api.library')
    def test_get_stats(self, mock_library, client):
        """Test getting library statistics."""
        mock_library.get_statistics.return_value = {
            "total_books": 5,
            "unique_authors": 3,
            "authors": ["Author A", "Author B", "Author C"]
        }
        
        response = client.get("/stats")
        assert response.status_code == 200
        
        data = response.json()
        assert data["total_books"] == 5
        assert data["unique_authors"] == 3
        assert len(data["authors"]) == 3


class TestAPIErrorHandling:
    """Test error handling in the API."""
    
    @pytest.fixture
    def client(self):
        return TestClient(app)
    
    @patch('api.library')
    def test_duplicate_book_error(self, mock_library, client):
        """Test handling duplicate book error."""
        from src.utils.exceptions import DuplicateBookError
        mock_library.add_book_by_isbn.side_effect = DuplicateBookError("Book exists")
        
        response = client.post("/books", json={"isbn": "1234567890"})
        assert response.status_code == 409
        
        data = response.json()
        assert "error" in data
    
    @patch('api.library')
    def test_api_error_handling(self, mock_library, client):
        """Test handling external API errors."""
        from src.utils.exceptions import APIError
        mock_library.add_book_by_isbn.side_effect = APIError("API failed")
        
        response = client.post("/books", json={"isbn": "1234567890"})
        assert response.status_code == 502
        
        data = response.json()
        assert data["error"] == "External API error"
    
    @patch('api.library')
    def test_invalid_isbn_error(self, mock_library, client):
        """Test handling invalid ISBN error."""
        from src.utils.exceptions import InvalidISBNError
        mock_library.add_book_by_isbn.side_effect = InvalidISBNError("Invalid ISBN")
        
        response = client.post("/books", json={"isbn": "1234567890"})
        assert response.status_code == 400


class TestAPIIntegration:
    """Integration tests for the complete API workflow."""
    
    @pytest.fixture
    def client(self):
        return TestClient(app)
    
    def test_complete_book_lifecycle(self, client):
        """Test complete book lifecycle through API."""
        # This would require a real library instance for full integration testing
        # For now, we'll test the endpoints exist and return expected structure
        
        # Test adding a book (mocked)
        with patch('api.library') as mock_library:
            test_book = Book("Lifecycle Test", "Test Author", "5555555555")
            mock_library.add_book_by_isbn.return_value = test_book
            mock_library.find_book.return_value = test_book
            mock_library.list_books.return_value = [test_book]
            
            # Add book
            response = client.post("/books", json={"isbn": "5555555555"})
            assert response.status_code == 201
            
            # Get book
            response = client.get("/books/5555555555")
            assert response.status_code == 200
            
            # List books
            response = client.get("/books")
            assert response.status_code == 200
            
            # Delete book
            response = client.delete("/books/5555555555")
            assert response.status_code == 200