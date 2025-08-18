# src/utils/exceptions.py

"""
Custom exceptions for the library management system.

These exceptions provide more specific error handling and better
user experience by giving meaningful error messages.
"""


class LibraryError(Exception):
    """
    Base exception for all library-related errors.
    
    This serves as the parent class for all our custom exceptions,
    making it easy to catch any library-specific error.
    """
    pass


class BookNotFoundError(LibraryError):
    """
    Raised when trying to access a book that doesn't exist in the library.
    
    This is thrown when searching for or trying to remove a book
    that can't be found by its ISBN.
    """
    pass


class DuplicateBookError(LibraryError):
    """
    Raised when trying to add a book that already exists in the library.
    
    Since ISBN should be unique, this prevents duplicate entries
    from being added to our library collection.
    """
    pass


class InvalidISBNError(LibraryError):
    """
    Raised when an invalid ISBN format is provided.
    
    This helps catch ISBN validation errors early in the process.
    """
    pass


class FileStorageError(LibraryError):
    """
    Raised when there are issues with reading or writing the storage file.
    
    This covers scenarios like permission issues, disk full,
    or corrupted data files.
    """
    pass


class APIError(LibraryError):
    """
    Raised when external API calls fail.
    
    This will be useful in Stage 2 when we integrate with the Open Library API.
    """
    pass