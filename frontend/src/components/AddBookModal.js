// src/components/AddBookModal.js

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { X, Search, Edit, BookOpen, Loader } from 'lucide-react';
import './AddBookModal.css';

const GENRE_OPTIONS = [
  'Fiction', 'Mystery', 'Romance', 'Children',
  'Science Fiction', 'Fantasy', 'Horror', 'Adventure',
  'Science', 'History', 'Philosophy', 'Biography'
];

const AddBookModal = ({ onClose, onAddBook, onAddBookManual }) => {
  const [activeTab, setActiveTab] = useState('api');
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    isbn: '', title: '', author: '', genre: ''
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      if (activeTab === 'api') {
        await onAddBook({ isbn: formData.isbn });
      } else {
        await onAddBookManual({
          title: formData.title,
          author: formData.author,
          isbn: formData.isbn,
          genre: formData.genre || undefined
        });
      }
      setFormData({ isbn: '', title: '', author: '', genre: '' });
    } catch (error) {
      console.error('Error adding book:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  return (
    <motion.div className="modal-overlay" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} onClick={onClose}>
      <motion.div className="add-book-modal" initial={{ scale: 0.8, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} exit={{ scale: 0.8, opacity: 0 }} onClick={(e) => e.stopPropagation()}>
        
        <div className="modal-header">
          <h2><BookOpen size={24} />Add New Book</h2>
          <button className="close-btn" onClick={onClose}><X size={20} /></button>
        </div>

        <div className="tab-navigation">
          <button className={`tab-btn ${activeTab === 'api' ? 'active' : ''}`} onClick={() => setActiveTab('api')}>
            <Search size={18} />ISBN Lookup
          </button>
          <button className={`tab-btn ${activeTab === 'manual' ? 'active' : ''}`} onClick={() => setActiveTab('manual')}>
            <Edit size={18} />Manual Entry
          </button>
        </div>

        <form onSubmit={handleSubmit} className="book-form">
          {activeTab === 'api' ? (
            <motion.div className="form-section" initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }}>
              <div className="form-description">
                <p>Enter an ISBN and we'll automatically fetch the book details. Books will be placed in "Unassigned" until you categorize them.</p>
              </div>
              
              <div className="form-group">
                <label htmlFor="isbn">ISBN</label>
                <input id="isbn" type="text" value={formData.isbn} onChange={(e) => handleInputChange('isbn', e.target.value)} placeholder="978-0-123456-78-9" required className="form-input" />
                <span className="form-hint">Enter ISBN-10 or ISBN-13 (with or without hyphens)</span>
              </div>
            </motion.div>
          ) : (
            <motion.div className="form-section" initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }}>
              <div className="form-description">
                <p>Manually enter book details and assign to a specific shelf category.</p>
              </div>
              
              <div className="form-group">
                <label htmlFor="title">Book Title</label>
                <input id="title" type="text" value={formData.title} onChange={(e) => handleInputChange('title', e.target.value)} placeholder="Enter book title" required className="form-input" />
              </div>

              <div className="form-group">
                <label htmlFor="author">Author</label>
                <input id="author" type="text" value={formData.author} onChange={(e) => handleInputChange('author', e.target.value)} placeholder="Enter author name" required className="form-input" />
              </div>

              <div className="form-group">
                <label htmlFor="manual-isbn">ISBN</label>
                <input id="manual-isbn" type="text" value={formData.isbn} onChange={(e) => handleInputChange('isbn', e.target.value)} placeholder="978-0-123456-78-9" required className="form-input" />
              </div>

              <div className="form-group">
                <label htmlFor="genre">Shelf Category</label>
                <select id="genre" value={formData.genre} onChange={(e) => handleInputChange('genre', e.target.value)} className="form-input">
                  <option value="">Select a category...</option>
                  {GENRE_OPTIONS.map(genre => (
                    <option key={genre} value={genre}>{genre}</option>
                  ))}
                </select>
                <span className="form-hint">Choose which floor/shelf to place this book</span>
              </div>
            </motion.div>
          )}

          <div className="form-actions">
            <button type="button" className="btn btn-secondary" onClick={onClose}>Cancel</button>
            <button type="submit" className="btn btn-primary" disabled={loading}>
              {loading ? (
                <><Loader className="spinning" size={16} />Adding...</>
              ) : (
                <><BookOpen size={16} />Add Book</>
              )}
            </button>
          </div>
        </form>

        <div className="modal-footer">
          <div className="help-text">
            {activeTab === 'api' ? (
              <p>💡 <strong>Tip:</strong> ISBN books go to 4th floor "Unassigned" section until manually categorized.</p>
            ) : (
              <p>💡 <strong>Tip:</strong> Choose a category to place your book directly on the correct floor.</p>
            )}
          </div>
        </div>
      </motion.div>
    </motion.div>
  );
};

export default AddBookModal;