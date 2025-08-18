// src/components/BookCard.js

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { X, Trash2, BookOpen, User, Hash, Edit, Save } from 'lucide-react';
import './BookCard.css';

const GENRE_OPTIONS = [
  'Fiction', 'Mystery', 'Romance', 'Children',
  'Science Fiction', 'Fantasy', 'Horror', 'Adventure',
  'Science', 'History', 'Philosophy', 'Biography', 'Unassigned'
];

const BookCard = ({ book, onDelete, onUpdate, onClose, expanded = false }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editedGenre, setEditedGenre] = useState(book.genre || 'Unassigned');

  const handleDelete = () => {
    if (window.confirm(`Are you sure you want to remove "${book.title}" from the library?`)) {
      onDelete(book.isbn);
    }
  };

  const handleSaveGenre = async () => {
    try {
      await onUpdate(book.isbn, { genre: editedGenre });
      setIsEditing(false);
    } catch (error) {
      console.error('Failed to update book genre:', error);
    }
  };

  return (
    <motion.div 
      className={`book-card ${expanded ? 'expanded' : ''}`}
      layout
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.9 }}
    >
      <div className="book-cover">
        <div className="cover-design">
          <div className="cover-title">{book.title}</div>
          <div className="cover-author">by {book.author}</div>
        </div>
        <div className="book-spine-shadow"></div>
      </div>

      <div className="book-details">
        <div className="book-header">
          <h3 className="book-title">
            <BookOpen size={18} />
            {book.title}
          </h3>
          {expanded && (
            <button className="close-btn" onClick={onClose}>
              <X size={20} />
            </button>
          )}
        </div>

        <div className="book-info">
          <div className="info-item">
            <User size={16} />
            <span className="info-label">Author:</span>
            <span className="info-value">{book.author}</span>
          </div>
          
          <div className="info-item">
            <Hash size={16} />
            <span className="info-label">ISBN:</span>
            <span className="info-value">{book.isbn}</span>
          </div>

          <div className="info-item">
            <Edit size={16} />
            <span className="info-label">Category:</span>
            {isEditing ? (
              <div className="genre-edit">
                <select 
                  value={editedGenre} 
                  onChange={(e) => setEditedGenre(e.target.value)}
                  className="genre-select"
                >
                  {GENRE_OPTIONS.map(genre => (
                    <option key={genre} value={genre}>{genre}</option>
                  ))}
                </select>
                <button onClick={handleSaveGenre} className="save-btn">
                  <Save size={14} />
                </button>
              </div>
            ) : (
              <span 
                className="info-value genre-clickable" 
                onClick={() => setIsEditing(true)}
              >
                {book.genre || 'Unassigned'} ✏️
              </span>
            )}
          </div>
        </div>

        {expanded && (
          <motion.div 
            className="book-actions"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
          >
            <motion.button
              className="delete-btn"
              onClick={handleDelete}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <Trash2 size={16} />
              Remove from Library
            </motion.button>
          </motion.div>
        )}

        {expanded && (
          <motion.div 
            className="book-metadata"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.3 }}
          >
            <div className="metadata-section">
              <h4>Library Information</h4>
              <div className="metadata-grid">
                <div className="metadata-item">
                  <span className="metadata-label">Added:</span>
                  <span className="metadata-value">Recently</span>
                </div>
                <div className="metadata-item">
                  <span className="metadata-label">Format:</span>
                  <span className="metadata-value">Physical</span>
                </div>
                <div className="metadata-item">
                  <span className="metadata-label">Status:</span>
                  <span className="metadata-value status-available">Available</span>
                </div>
                <div className="metadata-item">
                  <span className="metadata-label">Shelf:</span>
                  <span className="metadata-value">
                    {book.genre === 'Unassigned' ? '4th Floor' : 
                     ['Fiction', 'Mystery', 'Romance', 'Children'].includes(book.genre) ? 'Ground Floor' :
                     ['Science Fiction', 'Fantasy', 'Horror', 'Adventure'].includes(book.genre) ? '2nd Floor' :
                     ['Science', 'History', 'Philosophy', 'Biography'].includes(book.genre) ? '3rd Floor' : '4th Floor'}
                  </span>
                </div>
              </div>
            </div>
          </motion.div>
        )}
      </div>

      {!expanded && (
        <div className="book-corner-fold"></div>
      )}
    </motion.div>
  );
};

export default BookCard;