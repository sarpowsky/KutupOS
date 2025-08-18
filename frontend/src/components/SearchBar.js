// src/components/SearchBar.js

import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Search, X, BookOpen } from 'lucide-react';
import './SearchBar.css';

const SearchBar = ({ searchQuery, onSearchChange, books = [], onBookSelect }) => {
  const [showDropdown, setShowDropdown] = useState(false);
  const [filteredBooks, setFilteredBooks] = useState([]);
  const searchRef = useRef(null);

  useEffect(() => {
    if (searchQuery.trim() === '') {
      setFilteredBooks([]);
      setShowDropdown(false);
    } else {
      const filtered = books.filter(book =>
        book.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        book.author.toLowerCase().includes(searchQuery.toLowerCase()) ||
        book.isbn.toLowerCase().includes(searchQuery.toLowerCase())
      ).slice(0, 5); // Limit to 5 results
      
      setFilteredBooks(filtered);
      setShowDropdown(filtered.length > 0);
    }
  }, [searchQuery, books]);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (searchRef.current && !searchRef.current.contains(event.target)) {
        setShowDropdown(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleClear = () => {
    onSearchChange('');
    setShowDropdown(false);
  };

  const handleBookClick = (book) => {
    onBookSelect?.(book);
    setShowDropdown(false);
  };

  return (
    <div className="search-bar" ref={searchRef}>
      <div className="search-input-container">
        <Search className="search-icon" size={20} />
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => onSearchChange(e.target.value)}
          onFocus={() => searchQuery && filteredBooks.length > 0 && setShowDropdown(true)}
          placeholder="Search books by title, author, or ISBN..."
          className="search-input"
        />
        {searchQuery && (
          <motion.button
            className="clear-search"
            onClick={handleClear}
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            initial={{ opacity: 0, scale: 0 }}
            animate={{ opacity: 1, scale: 1 }}
          >
            <X size={16} />
          </motion.button>
        )}
      </div>
      
      <AnimatePresence>
        {showDropdown && (
          <motion.div
            className="search-dropdown"
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.2 }}
          >
            {filteredBooks.map((book, index) => (
              <motion.div
                key={book.isbn}
                className="search-result-item"
                onClick={() => handleBookClick(book)}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.05 }}
                whileHover={{ backgroundColor: 'rgba(141, 110, 99, 0.1)' }}
              >
                <BookOpen className="result-icon" size={16} />
                <div className="result-content">
                  <div className="result-title">{book.title}</div>
                  <div className="result-author">by {book.author}</div>
                </div>
                <div className="result-genre">{book.genre || 'Unassigned'}</div>
              </motion.div>
            ))}
            
            {filteredBooks.length > 0 && (
              <div className="search-footer">
                {filteredBooks.length} result{filteredBooks.length !== 1 ? 's' : ''} found
              </div>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default SearchBar;