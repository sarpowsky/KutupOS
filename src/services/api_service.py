# src/services/api_service.py

import time
import logging
from typing import Dict, Any
import requests
from cachetools import TTLCache
from src.utils.exceptions import APIError, InvalidISBNError

logger = logging.getLogger(__name__)


class OpenLibraryService:
    """Service for fetching book data from Open Library API."""
    
    BASE_URL = "https://openlibrary.org"
    TIMEOUT = 10.0
    MAX_RETRIES = 3
    CACHE_TTL = 3600
    
    def __init__(self):
        self.cache = TTLCache(maxsize=1000, ttl=self.CACHE_TTL)
        
    def _normalize_isbn(self, isbn: str) -> str:
        return isbn.replace("-", "").replace(" ", "").strip()
    
    def _validate_isbn_format(self, isbn: str) -> bool:
        clean_isbn = self._normalize_isbn(isbn)
        
        if len(clean_isbn) == 10:
            return clean_isbn[:9].isdigit() and (clean_isbn[9].isdigit() or clean_isbn[9] == 'X')
        elif len(clean_isbn) == 13:
            return clean_isbn.isdigit()
        
        return False
    
    def fetch_book_sync(self, isbn: str) -> Dict[str, Any]:
        """Fetch book information from Open Library API."""
        if not self._validate_isbn_format(isbn):
            raise InvalidISBNError(f"Invalid ISBN format: {isbn}")
        
        clean_isbn = self._normalize_isbn(isbn)
        
        # Check cache first
        if clean_isbn in self.cache:
            logger.info(f"Cache hit for ISBN: {clean_isbn}")
            return self.cache[clean_isbn]
        
        # Make API request with retry logic
        book_data = self._fetch_with_retry(clean_isbn)
        
        # Cache successful result
        self.cache[clean_isbn] = book_data
        logger.info(f"Cached book data for ISBN: {clean_isbn}")
        
        return book_data
    
    def _fetch_with_retry(self, isbn: str) -> Dict[str, Any]:
        """Fetch book data with retry logic."""
        url = f"{self.BASE_URL}/isbn/{isbn}.json"
        
        for attempt in range(1, self.MAX_RETRIES + 1):
            try:
                logger.debug(f"API request attempt {attempt} for ISBN: {isbn}")
                
                response = requests.get(url, timeout=self.TIMEOUT)
                
                if response.status_code == 200:
                    data = response.json()
                    return self._parse_book_data(data, isbn)
                elif response.status_code == 404:
                    raise APIError(f"Book not found for ISBN: {isbn}")
                else:
                    logger.warning(f"API returned status {response.status_code} for ISBN: {isbn}")
                    if attempt == self.MAX_RETRIES:
                        raise APIError(f"API request failed with status {response.status_code}")
                    time.sleep(2 ** attempt)
            
            except requests.RequestException as e:
                logger.error(f"Request error on attempt {attempt}: {e}")
                if attempt == self.MAX_RETRIES:
                    raise APIError(f"Network error after {self.MAX_RETRIES} attempts: {e}")
                time.sleep(2 ** attempt)
            
            except Exception as e:
                logger.error(f"Unexpected error on attempt {attempt}: {e}")
                raise APIError(f"Unexpected API error: {e}")
    
    def _parse_book_data(self, api_response: Dict[str, Any], isbn: str) -> Dict[str, Any]:
        """Parse and normalize API response data."""
        try:
            title = api_response.get("title", "").strip()
            if not title:
                raise APIError(f"No title found in API response for ISBN: {isbn}")
            
            authors = []
            if "authors" in api_response:
                for author_ref in api_response["authors"]:
                    if isinstance(author_ref, dict) and "key" in author_ref:
                        author_key = author_ref["key"]
                        author_name = author_key.split("/")[-1].replace("_", " ").title()
                        authors.append(author_name)
                    elif isinstance(author_ref, str):
                        authors.append(author_ref)
            
            if not authors:
                if "by_statement" in api_response:
                    authors = [api_response["by_statement"]]
                else:
                    authors = ["Unknown Author"]
            
            author = ", ".join(authors) if authors else "Unknown Author"
            
            book_data = {
                "title": title,
                "author": author,
                "isbn": isbn,
                "publication_date": api_response.get("publish_date"),
                "publisher": api_response.get("publishers", [None])[0] if api_response.get("publishers") else None,
                "pages": api_response.get("number_of_pages"),
                "subjects": api_response.get("subjects", [])[:5],
                "api_source": "Open Library"
            }
            
            logger.info(f"Successfully parsed book: {title} by {author}")
            return book_data
        
        except Exception as e:
            logger.error(f"Error parsing API response for ISBN {isbn}: {e}")
            raise APIError(f"Failed to parse API response: {e}")
    
    def clear_cache(self) -> None:
        self.cache.clear()
        logger.info("API cache cleared")
    
    def get_cache_stats(self) -> Dict[str, Any]:
        return {
            "cache_size": len(self.cache),
            "max_size": self.cache.maxsize,
            "ttl": self.cache.ttl
        }