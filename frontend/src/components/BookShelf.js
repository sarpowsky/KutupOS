// src/components/BookShelf.js

import React from 'react';
import { motion } from 'framer-motion';
import { getGenreColor, getRandomBookColor, getTextColor } from '../services/genreService';
import './BookShelf.css';

const BookShelf = ({ shelf, onBookClick, searchQuery }) => {
  const isBookHighlighted = (book) => {
    if (!searchQuery) return false;
    const query = searchQuery.toLowerCase();
    return (
      book.title.toLowerCase().includes(query) ||
      book.author.toLowerCase().includes(query) ||
      book.isbn.toLowerCase().includes(query)
    );
  };

  const capacity = shelf.capacity || 8;
  const isUnassigned = shelf.genre === 'Unassigned';
  const shelfCount = isUnassigned ? 2 : 1;
  const booksPerShelf = isUnassigned ? 12 : capacity;

  const renderShelf = (shelfIndex) => (
    <div key={shelfIndex} className="shelf-structure">
      <div className="shelf-board top-board"></div>
      
      <div className="books-container">
        {Array.from({ length: booksPerShelf }).map((_, slotIndex) => {
          const bookIndex = shelfIndex * booksPerShelf + slotIndex;
          const book = shelf.books[bookIndex];
          
          if (book) {
            const bookColor = getRandomBookColor(book.isbn);
            const textColor = getTextColor(bookColor);
            
            return (
              <motion.div
                key={book.isbn}
                className={`book-spine ${isBookHighlighted(book) ? 'highlighted' : ''}`}
                style={{ 
                  backgroundColor: bookColor,
                  height: `${60 + Math.random() * 20}px`
                }}
                initial={{ y: 20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ 
                  delay: slotIndex * 0.1,
                  type: "spring",
                  stiffness: 200
                }}
                whileHover={{ 
                  y: -5,
                  scale: 1.05,
                  transition: { duration: 0.2 }
                }}
                whileTap={{ scale: 0.95 }}
                onClick={() => onBookClick(book)}
              >
                <div className="book-author" style={{ color: textColor }}>
                  {book.author.length > 20 
                    ? book.author.substring(0, 20) + '...' 
                    : book.author
                  }
                </div>
                
                <div className="book-binding">
                  <div className="binding-line" style={{ backgroundColor: textColor }}></div>
                  <div className="binding-line" style={{ backgroundColor: textColor }}></div>
                </div>
              </motion.div>
            );
          } else {
            return (
              <div key={`empty-${shelfIndex}-${slotIndex}`} className="empty-slot">
                <div className="slot-indicator"></div>
              </div>
            );
          }
        })}
      </div>
      
      <div className="shelf-board bottom-board"></div>
      <div className="shelf-support left-support"></div>
      <div className="shelf-support right-support"></div>
    </div>
  );

  return (
    <div className="bookshelf">
      <div className="shelf-label">
        <span className="section-name">{shelf.genre}</span>
        <span className="book-count">{shelf.books.length}/{capacity}</span>
        {shelf.totalShelves > 1 && (
          <span className="shelf-number">Shelf {shelf.shelfNumber}/{shelf.totalShelves}</span>
        )}
      </div>

      {isUnassigned ? (
        <div className="unassigned-shelves">
          {Array.from({ length: shelfCount }).map((_, index) => renderShelf(index))}
        </div>
      ) : (
        renderShelf(0)
      )}

      <div className="genre-indicator" style={{ backgroundColor: getGenreColor(shelf.genre) }}>
        {shelf.genre}
      </div>
    </div>
  );
};

export default BookShelf;