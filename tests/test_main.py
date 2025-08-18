# tests/test_main.py

import pytest
from unittest.mock import Mock, patch, MagicMock
from rich.console import Console
import sys
import os

# Add the parent directory to sys.path to enable imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from main import LibraryApp
from src.models.book import Book
from src.utils.exceptions import BookNotFoundError, DuplicateBookError


class TestLibraryApp:
    """
    Test suite for the main LibraryApp class.
    
    These tests focus on the application logic and user interface handling.
    """
    
    @pytest.fixture
    def mock_library(self):
        """Mock library for testing app functionality."""
        library = Mock()
        library.list_books.return_value = []
        library.get_books_count.return_value = 0
        library.get_statistics.return_value = {
            "total_books": 0,
            "unique_authors": 0,
            "authors": []
        }
        library.filename = "test_library.json"
        return library
    
    @pytest.fixture
    def app_with_mock_library(self, mock_library):
        """LibraryApp instance with mocked library."""
        with patch('main.Library', return_value=mock_library):
            app = LibraryApp()
            app.library = mock_library
            return app
    
    def test_app_initialization(self):
        """Test LibraryApp initializes correctly."""
        with patch('main.Library') as mock_library_class:
            app = LibraryApp()
            
            assert app.running == True
            mock_library_class.assert_called_once()
    
    @patch('main.console.print')
    def test_display_welcome(self, mock_print, app_with_mock_library):
        """Test welcome message display."""
        app_with_mock_library.display_welcome()
        
        assert mock_print.called
    
    @patch('main.console.print')
    def test_display_menu(self, mock_print, app_with_mock_library):
        """Test menu display."""
        app_with_mock_library.display_menu()
        
        assert mock_print.called
    
    @patch('main.Prompt.ask')
    @patch('main.console.print')
    def test_add_book_interactive_success(self, mock_print, mock_ask, app_with_mock_library):
        """Test successful book addition through interactive interface."""
        # Mock user inputs
        mock_ask.side_effect = ["Test Title", "Test Author", "123456789"]
        
        app_with_mock_library.add_book_interactive()
        
        # Verify library.add_book was called with correct Book
        app_with_mock_library.library.add_book.assert_called_once()
        added_book = app_with_mock_library.library.add_book.call_args[0][0]
        assert isinstance(added_book, Book)
        assert added_book.title == "Test Title"
        assert added_book.author == "Test Author"
        assert added_book.isbn == "123456789"
    
    @patch('main.Prompt.ask')
    @patch('main.console.print')
    def test_add_book_interactive_empty_fields(self, mock_print, mock_ask, app_with_mock_library):
        """Test book addition with empty fields."""
        mock_ask.side_effect = ["", "Author", "ISBN"]
        
        app_with_mock_library.add_book_interactive()
        
        # Should not call add_book due to validation
        app_with_mock_library.library.add_book.assert_not_called()
    
    @patch('main.Prompt.ask')
    @patch('main.console.print')
    def test_add_book_interactive_duplicate_error(self, mock_print, mock_ask, app_with_mock_library):
        """Test handling duplicate book error."""
        mock_ask.side_effect = ["Title", "Author", "123456789"]
        app_with_mock_library.library.add_book.side_effect = DuplicateBookError("Book exists")
        
        app_with_mock_library.add_book_interactive()
        
        # Should print error message
        mock_print.assert_called()
    
    @patch('main.Prompt.ask')
    @patch('main.Confirm.ask')
    @patch('main.console.print')
    def test_delete_book_interactive_success(self, mock_print, mock_confirm, mock_ask, app_with_mock_library):
        """Test successful book deletion."""
        mock_ask.return_value = "123456789"
        mock_confirm.return_value = True
        
        # Mock finding the book
        mock_book = Book("Test", "Author", "123456789")
        app_with_mock_library.library.find_book.return_value = mock_book
        
        app_with_mock_library.delete_book_interactive()
        
        app_with_mock_library.library.find_book.assert_called_with("123456789")
        app_with_mock_library.library.remove_book.assert_called_with("123456789")
    
    @patch('main.Prompt.ask')
    @patch('main.console.print')
    def test_delete_book_interactive_not_found(self, mock_print, mock_ask, app_with_mock_library):
        """Test deletion of non-existent book."""
        mock_ask.return_value = "nonexistent"
        app_with_mock_library.library.find_book.return_value = None
        
        app_with_mock_library.delete_book_interactive()
        
        app_with_mock_library.library.remove_book.assert_not_called()
    
    @patch('main.Confirm.ask')
    @patch('main.Prompt.ask')
    @patch('main.console.print')
    def test_delete_book_interactive_cancelled(self, mock_print, mock_ask, mock_confirm, app_with_mock_library):
        """Test deletion cancelled by user."""
        mock_ask.return_value = "123456789"
        mock_confirm.return_value = False
        
        mock_book = Book("Test", "Author", "123456789")
        app_with_mock_library.library.find_book.return_value = mock_book
        
        app_with_mock_library.delete_book_interactive()
        
        app_with_mock_library.library.remove_book.assert_not_called()
    
    @patch('main.console.print')
    def test_list_books_interactive_empty_library(self, mock_print, app_with_mock_library):
        """Test listing books when library is empty."""
        app_with_mock_library.library.list_books.return_value = []
        
        app_with_mock_library.list_books_interactive()
        
        mock_print.assert_called()
    
    @patch('main.console.print')
    def test_list_books_interactive_with_books(self, mock_print, app_with_mock_library):
        """Test listing books when library has books."""
        books = [Book("Test1", "Author1", "111"), Book("Test2", "Author2", "222")]
        app_with_mock_library.library.list_books.return_value = books
        
        app_with_mock_library.list_books_interactive()
        
        mock_print.assert_called()
    
    @patch('main.Prompt.ask')
    @patch('main.console.print')
    def test_search_book_by_isbn_found(self, mock_print, mock_ask, app_with_mock_library):
        """Test searching book by ISBN - found."""
        mock_ask.side_effect = ["isbn", "123456789"]
        mock_book = Book("Found Book", "Author", "123456789")
        app_with_mock_library.library.find_book.return_value = mock_book
        
        app_with_mock_library.search_book_interactive()
        
        app_with_mock_library.library.find_book.assert_called_with("123456789")
    
    @patch('main.Prompt.ask')
    @patch('main.console.print')
    def test_search_book_by_isbn_not_found(self, mock_print, mock_ask, app_with_mock_library):
        """Test searching book by ISBN - not found."""
        mock_ask.side_effect = ["isbn", "nonexistent"]
        app_with_mock_library.library.find_book.return_value = None
        
        app_with_mock_library.search_book_interactive()
        
        app_with_mock_library.library.find_book.assert_called_with("nonexistent")
    
    @patch('main.Prompt.ask')
    @patch('main.console.print')
    def test_search_book_by_keyword(self, mock_print, mock_ask, app_with_mock_library):
        """Test searching book by keyword."""
        mock_ask.side_effect = ["keyword", "test query"]
        found_books = [Book("Test Book", "Author", "123")]
        app_with_mock_library.library.search_books.return_value = found_books
        
        app_with_mock_library.search_book_interactive()
        
        app_with_mock_library.library.search_books.assert_called_with("test query")
    
    @patch('main.console.print')
    def test_show_statistics(self, mock_print, app_with_mock_library):
        """Test displaying library statistics."""
        app_with_mock_library.library.get_statistics.return_value = {
            "total_books": 5,
            "unique_authors": 3,
            "authors": ["Author A", "Author B", "Author C"]
        }
        
        app_with_mock_library.show_statistics()
        
        mock_print.assert_called()
    
    def test_handle_menu_choice_valid_options(self, app_with_mock_library):
        """Test handling valid menu choices."""
        with patch.object(app_with_mock_library, 'add_book_interactive') as mock_add:
            app_with_mock_library.handle_menu_choice("1")
            mock_add.assert_called_once()
        
        with patch.object(app_with_mock_library, 'delete_book_interactive') as mock_delete:
            app_with_mock_library.handle_menu_choice("2")
            mock_delete.assert_called_once()
        
        with patch.object(app_with_mock_library, 'list_books_interactive') as mock_list:
            app_with_mock_library.handle_menu_choice("3")
            mock_list.assert_called_once()
    
    @patch('main.console.print')
    def test_handle_menu_choice_invalid(self, mock_print, app_with_mock_library):
        """Test handling invalid menu choice."""
        app_with_mock_library.handle_menu_choice("invalid")
        
        mock_print.assert_called()
    
    @patch('main.Confirm.ask')
    def test_exit_application_confirmed(self, mock_confirm, app_with_mock_library):
        """Test application exit when confirmed."""
        mock_confirm.return_value = True
        
        app_with_mock_library.exit_application()
        
        assert app_with_mock_library.running == False
    
    @patch('main.Confirm.ask')
    def test_exit_application_cancelled(self, mock_confirm, app_with_mock_library):
        """Test application exit when cancelled."""
        mock_confirm.return_value = False
        
        app_with_mock_library.exit_application()
        
        assert app_with_mock_library.running == True
    
    @patch('main.Prompt.ask')
    @patch('main.console.print')
    @patch('main.console.clear')
    def test_run_main_loop_exit(self, mock_clear, mock_print, mock_ask, app_with_mock_library):
        """Test main run loop with exit option."""
        mock_ask.side_effect = ["6"]  # Exit option
        
        with patch.object(app_with_mock_library, 'exit_application') as mock_exit:
            mock_exit.side_effect = lambda: setattr(app_with_mock_library, 'running', False)
            app_with_mock_library.run()
            
            mock_exit.assert_called_once()
    
    @patch('main.Prompt.ask')
    @patch('main.console.print')
    def test_run_keyboard_interrupt(self, mock_print, mock_ask, app_with_mock_library):
        """Test handling keyboard interrupt during main loop."""
        mock_ask.side_effect = KeyboardInterrupt()
        
        with patch.object(app_with_mock_library, 'exit_application') as mock_exit:
            mock_exit.side_effect = lambda: setattr(app_with_mock_library, 'running', False)
            app_with_mock_library.run()
            
            mock_exit.assert_called_once()


@patch('main.setup_logging')
@patch('main.LibraryApp')
def test_main_function_success(mock_app_class, mock_setup_logging):
    """Test main function executes successfully."""
    from main import main
    
    mock_app = Mock()
    mock_app_class.return_value = mock_app
    
    main()
    
    mock_setup_logging.assert_called_once()
    mock_app_class.assert_called_once()
    mock_app.run.assert_called_once()


@patch('main.setup_logging')
@patch('main.LibraryApp')
@patch('main.sys.exit')
def test_main_function_exception(mock_exit, mock_app_class, mock_setup_logging):
    """Test main function handles exceptions."""
    from main import main
    
    mock_app_class.side_effect = Exception("Test error")
    
    main()
    
    mock_exit.assert_called_with(1)