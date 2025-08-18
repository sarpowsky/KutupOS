// src/components/FloorSelector.js

import React from 'react';
import { motion } from 'framer-motion';
import './FloorSelector.css';

const FloorSelector = ({ floors, currentFloor, onFloorChange }) => {
  return (
    <div className="floor-selector">
      <div className="floor-tabs">
        {floors.map((floor, index) => (
          <motion.button
            key={floor.id}
            className={`floor-tab ${currentFloor === index ? 'active' : ''}`}
            onClick={() => onFloorChange(index)}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <div className="floor-name">{floor.name}</div>
            <div className="floor-count">
              {floor.sections?.length || 0} sections
            </div>
          </motion.button>
        ))}
      </div>
    </div>
  );
};

export default FloorSelector;