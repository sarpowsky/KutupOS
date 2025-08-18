// src/components/StatsDashboard.js

import React from 'react';
import { motion } from 'framer-motion';
import { X, BookOpen, Users, TrendingUp, BarChart3 } from 'lucide-react';
import './StatsDashboard.css';

const StatsDashboard = ({ stats, totalBooks, onClose }) => {
  return (
    <motion.div
      className="modal-overlay"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      onClick={onClose}
    >
      <motion.div
        className="stats-dashboard"
        initial={{ scale: 0.8, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        exit={{ scale: 0.8, opacity: 0 }}
        onClick={(e) => e.stopPropagation()}
      >
        <div className="dashboard-header">
          <h2>
            <BarChart3 size={24} />
            Library Statistics
          </h2>
          <button className="close-btn" onClick={onClose}>
            <X size={20} />
          </button>
        </div>

        <div className="stats-grid">
          <motion.div 
            className="stat-card"
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.1 }}
          >
            <div className="stat-icon">
              <BookOpen size={32} />
            </div>
            <div className="stat-content">
              <h3>{totalBooks}</h3>
              <p>Total Books</p>
            </div>
          </motion.div>

          <motion.div 
            className="stat-card"
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.2 }}
          >
            <div className="stat-icon">
              <Users size={32} />
            </div>
            <div className="stat-content">
              <h3>{stats.unique_authors || 0}</h3>
              <p>Unique Authors</p>
            </div>
          </motion.div>

          <motion.div 
            className="stat-card"
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.3 }}
          >
            <div className="stat-icon">
              <TrendingUp size={32} />
            </div>
            <div className="stat-content">
              <h3>{Math.ceil(totalBooks / 8)}</h3>
              <p>Active Shelves</p>
            </div>
          </motion.div>
        </div>

        <div className="authors-section">
          <h3>Top Authors</h3>
          <div className="authors-list">
            {(stats.authors || []).slice(0, 10).map((author, index) => (
              <motion.div
                key={author}
                className="author-item"
                initial={{ x: -20, opacity: 0 }}
                animate={{ x: 0, opacity: 1 }}
                transition={{ delay: 0.4 + index * 0.05 }}
              >
                <span className="author-rank">#{index + 1}</span>
                <span className="author-name">{author}</span>
              </motion.div>
            ))}
          </div>
        </div>
      </motion.div>
    </motion.div>
  );
};

export default StatsDashboard;