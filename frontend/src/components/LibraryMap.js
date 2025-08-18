// src/components/LibraryMap.js

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { MapPin, Coffee, Users, ArrowUpDown, Info } from 'lucide-react';
import BookShelf from './BookShelf';
import BookCard from './BookCard';
import FloorSelector from './FloorSelector';
import { detectGenre } from '../services/genreService';
import './LibraryMap.css';

const LibraryMap = ({ books, onDeleteBook, onUpdateBook, searchQuery }) => {
  const [selectedBook, setSelectedBook] = useState(null);
  const [currentFloor, setCurrentFloor] = useState(0);
  const [floors, setFloors] = useState([]);
  const [filteredBooks, setFilteredBooks] = useState([]);

  useEffect(() => {
    if (!searchQuery) {
      setFilteredBooks(books);
    } else {
      const query = searchQuery.toLowerCase();
      const filtered = books.filter(book =>
        book.title.toLowerCase().includes(query) ||
        book.author.toLowerCase().includes(query) ||
        book.isbn.toLowerCase().includes(query)
      );
      setFilteredBooks(filtered);
    }
  }, [books, searchQuery]);

  useEffect(() => {
    const booksWithGenres = filteredBooks.map(book => ({
      ...book,
      genre: book.genre || detectGenre(book)
    }));

    const genreGroups = booksWithGenres.reduce((acc, book) => {
      if (!acc[book.genre]) acc[book.genre] = [];
      acc[book.genre].push(book);
      return acc;
    }, {});

    const floorConfigs = [
      {
        id: 0, name: 'Ground Floor',
        genres: ['Fiction', 'Mystery', 'Romance', 'Children'],
        layout: 'main-hall', shelfCapacity: 8,
        amenities: [
          { type: 'reception', label: 'Reception', icon: Info },
          { type: 'reading', label: 'Reading Area', icon: Coffee },
          { type: 'stairs', label: 'Stairs', icon: ArrowUpDown }
        ]
      },
      {
        id: 1, name: 'Second Floor',
        genres: ['Science Fiction', 'Fantasy', 'Horror', 'Adventure'],
        layout: 'genre-wings', shelfCapacity: 8,
        amenities: [
          { type: 'study', label: 'Study Pods', icon: Users },
          { type: 'reading', label: 'Quiet Zone', icon: Coffee },
          { type: 'stairs', label: 'Stairs', icon: ArrowUpDown }
        ]
      },
      {
        id: 2, name: 'Third Floor',
        genres: ['Science', 'History', 'Philosophy', 'Biography'],
        layout: 'study-area', shelfCapacity: 8,
        amenities: [
          { type: 'study', label: 'Research Area', icon: Users },
          { type: 'info', label: 'Information', icon: Info },
          { type: 'stairs', label: 'Stairs', icon: ArrowUpDown }
        ]
      },
      {
        id: 3, name: 'Fourth Floor',
        genres: ['Unassigned'], layout: 'unassigned-area', shelfCapacity: 24,
        amenities: [
          { type: 'info', label: 'Categorization', icon: Info },
          { type: 'reading', label: 'Sorting Area', icon: Coffee }
        ]
      }
    ];

    const organizedFloors = floorConfigs.map(floor => ({
      ...floor,
      sections: createSections(genreGroups, floor.genres, floor.shelfCapacity)
    }));

    setFloors(organizedFloors);
  }, [filteredBooks]);

  const createSections = (genreGroups, genres, capacity) => {
    const sections = [];
    
    genres.forEach((genre, genreIndex) => {
      const booksInGenre = genreGroups[genre] || [];
      const shelvesNeeded = Math.max(1, Math.ceil(booksInGenre.length / capacity));
      
      for (let i = 0; i < shelvesNeeded; i++) {
        const shelfBooks = booksInGenre.slice(i * capacity, (i + 1) * capacity);
        sections.push({
          id: `${genre}-${i}`,
          genre, books: shelfBooks, shelfNumber: i + 1, totalShelves: shelvesNeeded,
          capacity, position: { row: Math.floor(genreIndex / 2), col: genreIndex % 2, shelf: i }
        });
      }
    });

    return sections;
  };

  const renderAmenity = (amenity, index) => {
    const IconComponent = amenity.icon;
    
    return (
      <motion.div
        key={amenity.type + index}
        className={`floor-amenity ${amenity.type}-area`}
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 + index * 0.1 }}
      >
        <IconComponent className="amenity-icon" size={24} />
        <span className="amenity-label">{amenity.label}</span>
        
        {amenity.type === 'reception' && <div className="reception-desk"></div>}
        {amenity.type === 'reading' && (
          <div className="tables-group">
            <div className="table"></div>
            <div className="table"></div>
          </div>
        )}
        {amenity.type === 'study' && (
          <div className="study-pods">
            <div className="study-pod"></div>
            <div className="study-pod"></div>
            <div className="study-pod"></div>
          </div>
        )}
        {amenity.type === 'stairs' && (
          <div className="stairs-icon">
            <div className="stair-step" style={{'--step': 0}}></div>
            <div className="stair-step" style={{'--step': 1}}></div>
            <div className="stair-step" style={{'--step': 2}}></div>
          </div>
        )}
        {amenity.type === 'info' && <div className="desk-surface"></div>}
      </motion.div>
    );
  };

  const handleBookClick = (book) => setSelectedBook(book);
  const handleDeleteBook = async (isbn) => { await onDeleteBook(isbn); setSelectedBook(null); };
  const handleUpdateBook = async (isbn, updates) => { await onUpdateBook(isbn, updates); setSelectedBook(null); };

  const currentFloorData = floors[currentFloor];

  return (
    <div className="library-map">
      <div className="library-header">
        <h2>Digital Library</h2>
        <div className="library-stats">
          <span>{books.length} Books</span>
          <span>{floors.reduce((acc, floor) => acc + floor.sections?.length || 0, 0)} Shelves</span>
          {searchQuery && <span>Search Results</span>}
        </div>
      </div>

      <FloorSelector floors={floors} currentFloor={currentFloor} onFloorChange={setCurrentFloor} />

      <AnimatePresence mode="wait">
        {currentFloorData && (
          <motion.div
            key={currentFloor}
            className={`floor-layout ${currentFloorData.layout}`}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.5 }}
          >
            <div className="floor-info">
              <h3>{currentFloorData.name}</h3>
              <span>{currentFloorData.sections?.length || 0} sections</span>
            </div>

            <div className="floor-content">
              <div className="sections-container">
                {currentFloorData.sections?.map((section, index) => (
                  <motion.div
                    key={section.id}
                    className="section-wrapper"
                    initial={{ opacity: 0, scale: 0.8 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: index * 0.1 }}
                  >
                    <BookShelf shelf={section} onBookClick={handleBookClick} searchQuery={searchQuery} />
                  </motion.div>
                )) || (
                  <div className="empty-floor">
                    <p>No books on this floor yet</p>
                  </div>
                )}
              </div>

              <div className="floor-amenities">
                {currentFloorData.amenities?.map((amenity, index) => renderAmenity(amenity, index))}
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      <AnimatePresence>
        {selectedBook && (
          <motion.div
            className="book-modal-overlay"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={() => setSelectedBook(null)}
          >
            <motion.div
              className="book-modal"
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.8, opacity: 0 }}
              onClick={(e) => e.stopPropagation()}
            >
              <BookCard
                book={selectedBook} onDelete={handleDeleteBook} onUpdate={handleUpdateBook}
                onClose={() => setSelectedBook(null)} expanded={true}
              />
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default LibraryMap;