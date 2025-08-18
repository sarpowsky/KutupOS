// src/components/Header.js

import React from 'react';
import { motion } from 'framer-motion';
import { Library, BookOpen } from 'lucide-react';
import './Header.css';

const Header = () => {
  return (
    <motion.header 
      className="app-header"
      initial={{ y: -50, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.6 }}
    >
      <div className="header-content">
        <div className="logo">
          <Library size={32} className="logo-icon" />
          <div className="logo-text">
            <h1>BookNest</h1>
            <span className="tagline">Your Personal Library Sanctuary</span>
          </div>
        </div>
        
        <div className="header-decoration">
          <BookOpen className="floating-book" size={24} />
        </div>
      </div>
      
      <div className="header-shadow"></div>
    </motion.header>
  );
};

export default Header;