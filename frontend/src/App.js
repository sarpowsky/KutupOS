// src/App.js

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Toaster, toast } from 'react-hot-toast';
import { Plus, BarChart3, BookOpen } from 'lucide-react';

import LibraryMap from './components/LibraryMap';
import AddBookModal from './components/AddBookModal';
import SearchBar from './components/SearchBar';
import StatsDashboard from './components/StatsDashboard';
import Header from './components/Header';
import * as api from './services/api';
import './App.css';

function App() {
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [filteredBooks, setFilteredBooks] = useState([]);
  const [showAddModal, setShowAddModal] = useState(false);
  const [showStats, setShowStats] = useState(false);
  const [stats, setStats] = useState(null);

  useEffect(() => {
    loadBooks();
  }, []);

  useEffect(() => {
    if (searchQuery.trim() === '') {
      setFilteredBooks(books);
    } else {
      const filtered = books.filter(book =>
        book.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        book.author.toLowerCase().includes(searchQuery.toLowerCase()) ||
        book.isbn.toLowerCase().includes(searchQuery.toLowerCase())
      );
      setFilteredBooks(filtered);
    }
  }, [books, searchQuery]);

  const loadBooks = async () => {
    try {
      setLoading(true);
      const response = await api.getBooks();
      setBooks(response.books);
      if (response.books.length > 0) {
        toast.success(`Loaded ${response.books.length} books`);
      }
    } catch (error) {
      toast.error('Failed to load books');
      console.error('Error loading books:', error);
    } finally {
      setLoading(false);
    }
  };

  const addBook = async (bookData) => {
    try {
      const newBook = await api.addBook(bookData);
      setBooks(prev => [...prev, { ...newBook, genre: 'Unassigned' }]);
      toast.success(`Added: ${newBook.title}`);
      setShowAddModal(false);
    } catch (error) {
      toast.error(error.message || 'Failed to add book');
    }
  };

  const addBookManual = async (bookData) => {
    try {
      const newBook = await api.addBookManual(bookData);
      setBooks(prev => [...prev, newBook]);
      toast.success(`Added: ${newBook.title}`);
      setShowAddModal(false);
    } catch (error) {
      toast.error(error.message || 'Failed to add book manually');
    }
  };

  const updateBook = async (isbn, updates) => {
    try {
      const updatedBook = await api.updateBook(isbn, updates);
      setBooks(prev => prev.map(book => 
        book.isbn === isbn ? { ...book, ...updatedBook } : book
      ));
      toast.success('Book updated successfully');
    } catch (error) {
      toast.error('Failed to update book');
    }
  };

  const deleteBook = async (isbn) => {
    try {
      await api.deleteBook(isbn);
      setBooks(prev => prev.filter(book => book.isbn !== isbn));
      toast.success('Book removed from library');
    } catch (error) {
      toast.error('Failed to delete book');
    }
  };

  const loadStats = async () => {
    try {
      const statsData = await api.getStats();
      setStats(statsData);
      setShowStats(true);
    } catch (error) {
      toast.error('Failed to load statistics');
    }
  };

  const handleBookSelect = (book) => {
    // Optional: You can add logic here to navigate to the book's floor
    console.log('Selected book:', book);
  };

  return (
    <div className="app">
      <Toaster 
        position="top-right"
        toastOptions={{
          duration: 3000,
          style: {
            background: '#2d1810',
            color: '#f4f1ea',
            border: '1px solid #8b4513'
          }
        }}
      />
      
      <Header />
      
      <main className="main-content">
        <motion.div 
          className="control-panel"
          initial={{ y: -20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.5 }}
        >
          <div className="control-left">
            <SearchBar 
              searchQuery={searchQuery}
              onSearchChange={setSearchQuery}
              books={books}
              onBookSelect={handleBookSelect}
            />
          </div>
          
          <div className="control-right">
            <motion.button
              className="control-btn stats-btn"
              onClick={loadStats}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <BarChart3 size={20} />
              Statistics
            </motion.button>
            
            <motion.button
              className="control-btn add-btn"
              onClick={() => setShowAddModal(true)}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <Plus size={20} />
              Add Book
            </motion.button>
          </div>
        </motion.div>

        {loading && (
          <motion.div 
            className="loading-container"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
          >
            <div className="loading-spinner">
              <BookOpen className="spinning-book" size={48} />
              <p>Loading your library...</p>
            </div>
          </motion.div>
        )}

        {!loading && (
          <LibraryMap
            books={filteredBooks}
            onDeleteBook={deleteBook}
            onUpdateBook={updateBook}
            searchQuery={searchQuery}
          />
        )}
      </main>

      <AnimatePresence>
        {showAddModal && (
          <AddBookModal
            onClose={() => setShowAddModal(false)}
            onAddBook={addBook}
            onAddBookManual={addBookManual}
          />
        )}
        
        {showStats && stats && (
          <StatsDashboard
            stats={stats}
            totalBooks={books.length}
            onClose={() => setShowStats(false)}
          />
        )}
      </AnimatePresence>
    </div>
  );
}

export default App;