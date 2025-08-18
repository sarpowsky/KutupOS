# main.py

import logging
import sys
from pathlib import Path
from typing import Optional

# Rich library imports for beautiful terminal output
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.text import Text
from rich import print as rprint

# Our library components
from src.models.book import Book
from src.services.library import Library
from src.utils.exceptions import (
    LibraryError, BookNotFoundError, DuplicateBookError, 
    InvalidISBNError, FileStorageError, APIError
)


# Set up logging configuration
def setup_logging() -> None:
    """Configure logging for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('library_app.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )


# Initialize rich console for beautiful output
console = Console()


class LibraryApp:
    """
    Main application class that handles the user interface and menu system.
    
    This class orchestrates the entire application flow and provides
    a clean interface between the user and our library system.
    """
    
    def __init__(self) -> None:
        """Initialize the application with a library instance."""
        self.library = Library()
        self.running = True
    
    def display_welcome(self) -> None:
        """Show a welcoming banner when the application starts."""
        welcome_text = Text("📚 Library Management System", style="bold magenta")
        welcome_panel = Panel(
            welcome_text,
            subtitle="Manage your book collection with ease",
            border_style="blue"
        )
        console.print(welcome_panel)
        console.print()
    
    def display_menu(self) -> None:
        """Display the main menu options to the user."""
        menu_table = Table(title="Main Menu", show_header=False, border_style="green")
        menu_table.add_column("Option", style="cyan", width=4)
        menu_table.add_column("Description", style="white")
        
        menu_options = [
            ("1", "📖 Add Book (API)"),
            ("2", "📝 Add Book (Manual)"),
            ("3", "🗑️  Delete Book"),
            ("4", "📋 List All Books"),
            ("5", "🔍 Search Book"),
            ("6", "📊 Library Statistics"),
            ("7", "❌ Exit")
        ]
        
        for option, description in menu_options:
            menu_table.add_row(option, description)
        
        console.print(menu_table)
        console.print()
    
    def add_book_interactive(self) -> None:
        """Handle interactive book addition via API with ISBN only."""
        try:
            console.print("\n[bold cyan]Adding a new book via API[/bold cyan]")
            console.print("📡 Just enter the ISBN - we'll fetch title and author automatically!")
            
            isbn = Prompt.ask("🔢 Enter book ISBN")
            
            if not isbn.strip():
                console.print("[bold red]❌ ISBN is required![/bold red]")
                return
            
            # Show loading message
            with console.status("[bold green]Fetching book data from Open Library..."):
                book = self.library.add_book_by_isbn(isbn.strip())
            
            console.print(f"[bold green]✅ Successfully added: {book}[/bold green]")
            
        except DuplicateBookError as e:
            console.print(f"[bold red]❌ {e}[/bold red]")
        except InvalidISBNError as e:
            console.print(f"[bold red]❌ {e}[/bold red]")
            console.print("💡 Try manual entry option if ISBN format is unusual")
        except APIError as e:
            console.print(f"[bold red]❌ API Error: {e}[/bold red]")
            console.print("💡 Try manual entry or check your internet connection")
        except Exception as e:
            console.print(f"[bold red]❌ Unexpected error: {e}[/bold red]")
    
    def add_book_manual_interactive(self) -> None:
        """Handle manual book addition with user input validation."""
        try:
            console.print("\n[bold cyan]Adding a new book manually[/bold cyan]")
            
            # Get book information from user
            title = Prompt.ask("📖 Enter book title")
            author = Prompt.ask("👤 Enter book author")
            isbn = Prompt.ask("🔢 Enter book ISBN")
            
            # Validate inputs aren't empty
            if not all([title.strip(), author.strip(), isbn.strip()]):
                console.print("[bold red]❌ All fields are required![/bold red]")
                return
            
            # Create and add the book
            book = self.library.add_book_manual(title=title, author=author, isbn=isbn)
            console.print(f"[bold green]✅ Successfully added: {book}[/bold green]")
            
        except DuplicateBookError as e:
            console.print(f"[bold red]❌ {e}[/bold red]")
        except ValueError as e:
            console.print(f"[bold red]❌ Invalid input: {e}[/bold red]")
        except Exception as e:
            console.print(f"[bold red]❌ Unexpected error: {e}[/bold red]")
    
    def delete_book_interactive(self) -> None:
        """Handle interactive book deletion."""
        try:
            console.print("\n[bold cyan]Removing a book[/bold cyan]")
            
            isbn = Prompt.ask("🔢 Enter ISBN of book to remove")
            
            if not isbn.strip():
                console.print("[bold red]❌ ISBN is required![/bold red]")
                return
            
            # Find the book first to show user what will be deleted
            book = self.library.find_book(isbn)
            if book is None:
                console.print(f"[bold red]❌ No book found with ISBN: {isbn}[/bold red]")
                return
            
            # Confirm deletion
            console.print(f"Found book: [bold]{book}[/bold]")
            if Confirm.ask("Are you sure you want to delete this book?"):
                self.library.remove_book(isbn)
                console.print(f"[bold green]✅ Successfully removed: {book}[/bold green]")
            else:
                console.print("[yellow]Deletion cancelled[/yellow]")
                
        except BookNotFoundError as e:
            console.print(f"[bold red]❌ {e}[/bold red]")
        except Exception as e:
            console.print(f"[bold red]❌ Unexpected error: {e}[/bold red]")
    
    def list_books_interactive(self) -> None:
        """Display all books in a formatted table."""
        books = self.library.list_books()
        
        if not books:
            console.print("[yellow]📚 Your library is empty. Add some books to get started![/yellow]")
            return
        
        # Create a beautiful table for displaying books
        books_table = Table(title=f"Library Collection ({len(books)} books)", border_style="blue")
        books_table.add_column("Title", style="cyan", min_width=20)
        books_table.add_column("Author", style="magenta", min_width=15)
        books_table.add_column("ISBN", style="green", min_width=13)
        
        for book in books:
            books_table.add_row(book.title, book.author, book.isbn)
        
        console.print(books_table)
    
    def search_book_interactive(self) -> None:
        """Handle interactive book searching."""
        try:
            console.print("\n[bold cyan]Search for a book[/bold cyan]")
            
            search_type = Prompt.ask(
                "Search by", 
                choices=["isbn", "keyword"], 
                default="isbn"
            )
            
            if search_type == "isbn":
                isbn = Prompt.ask("🔢 Enter ISBN to search for")
                book = self.library.find_book(isbn)
                
                if book:
                    console.print(f"[bold green]📖 Found: {book}[/bold green]")
                else:
                    console.print(f"[bold red]❌ No book found with ISBN: {isbn}[/bold red]")
            
            else:  # keyword search
                query = Prompt.ask("🔍 Enter search term (title, author, or ISBN)")
                books = self.library.search_books(query)
                
                if books:
                    console.print(f"[bold green]Found {len(books)} book(s):[/bold green]")
                    for book in books:
                        console.print(f"  📖 {book}")
                else:
                    console.print(f"[bold red]❌ No books found matching: {query}[/bold red]")
                    
        except Exception as e:
            console.print(f"[bold red]❌ Search error: {e}[/bold red]")
    
    def show_statistics(self) -> None:
        """Display library statistics."""
        stats = self.library.get_statistics()
        
        stats_panel = Panel(
            f"📚 Total Books: {stats['total_books']}\n"
            f"👥 Unique Authors: {stats['unique_authors']}\n"
            f"📁 Storage File: {self.library.filename}",
            title="Library Statistics",
            border_style="yellow"
        )
        
        console.print(stats_panel)
        
        # Show top authors if we have books
        if stats['authors']:
            console.print("\n[bold]Authors in your library:[/bold]")
            for author in stats['authors'][:10]:  # Show first 10 authors
                console.print(f"  👤 {author}")
            
            if len(stats['authors']) > 10:
                console.print(f"  ... and {len(stats['authors']) - 10} more")
    
    def handle_menu_choice(self, choice: str) -> None:
        """Process the user's menu selection."""
        menu_actions = {
            "1": self.add_book_interactive,
            "2": self.add_book_manual_interactive,
            "3": self.delete_book_interactive,
            "4": self.list_books_interactive,
            "5": self.search_book_interactive,
            "6": self.show_statistics,
            "7": self.exit_application
        }
        
        action = menu_actions.get(choice)
        if action:
            action()
        else:
            console.print("[bold red]❌ Invalid choice. Please select 1-7.[/bold red]")
    
    def exit_application(self) -> None:
        """Handle application exit with confirmation."""
        if Confirm.ask("Are you sure you want to exit?"):
            console.print("[bold green]👋 Thank you for using Library Management System![/bold green]")
            self.running = False
    
    def run(self) -> None:
        """Main application loop that handles the user interface."""
        self.display_welcome()
        
        while self.running:
            try:
                self.display_menu()
                choice = Prompt.ask("Select an option (1-7)", default="4")
                
                console.print()  # Add some spacing
                self.handle_menu_choice(choice)
                console.print()  # Add spacing after each operation
                
                # Pause before showing menu again (except for exit)
                if self.running and choice != "6":
                    Prompt.ask("Press Enter to continue", default="")
                    console.clear()
                
            except KeyboardInterrupt:
                console.print("\n[yellow]Interrupted by user[/yellow]")
                self.exit_application()
            except Exception as e:
                console.print(f"[bold red]❌ Unexpected error: {e}[/bold red]")
                logging.error(f"Unexpected error in main loop: {e}")


def main() -> None:
    """Entry point of the application."""
    # Set up logging
    setup_logging()
    
    try:
        # Create and run the application
        app = LibraryApp()
        app.run()
        
    except Exception as e:
        console.print(f"[bold red]❌ Fatal error: {e}[/bold red]")
        logging.critical(f"Fatal error in main: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()