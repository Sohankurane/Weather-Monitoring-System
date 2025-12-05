import React, { useState } from 'react';
import { useCityManager } from './CityManager.hook';
import './CityManager.css';

export const CityManager = ({ cities, onAddCity, onRemoveCity }) => {
  const [showDropdown, setShowDropdown] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  
  // Popular cities list
  const popularCities = [
    'Mumbai', 'Delhi', 'Bangalore', 'Pune', 'Chennai',
    'Kolkata', 'Hyderabad', 'Ahmedabad', 'Jaipur', 'Surat',
    'Lucknow', 'Kanpur', 'Nagpur', 'Indore', 'Thane',
    'Bhopal', 'Visakhapatnam', 'Patna', 'Vadodara', 'Ghaziabad'
  ];

  const filteredCities = popularCities.filter(city => 
    city.toLowerCase().includes(searchTerm.toLowerCase()) &&
    !cities.includes(city)
  );

  const handleAddCity = (city) => {
    if (cities.length < 5) {
      onAddCity(city);
      setSearchTerm('');
      setShowDropdown(false);
    } else {
      alert('Maximum 5 cities allowed!');
    }
  };

  return (
    <div className="city-manager">
      <div className="city-list">
        {cities.map((city, index) => (
          <div key={index} className="city-chip">
            <span className="city-name">{city}</span>
            <button 
              className="remove-btn"
              onClick={() => onRemoveCity(city)}
              title="Remove city"
            >
              ✕
            </button>
          </div>
        ))}
        
        {cities.length < 5 && (
          <button 
            className="add-city-btn"
            onClick={() => setShowDropdown(!showDropdown)}
          >
            + Add City
          </button>
        )}
      </div>

      {showDropdown && (
        <div className="city-dropdown">
          <input
            type="text"
            className="city-search-input"
            placeholder="Search for a city..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            autoFocus
          />
          <div className="city-options">
            {filteredCities.length > 0 ? (
              filteredCities.map((city, index) => (
                <div
                  key={index}
                  className="city-option"
                  onClick={() => handleAddCity(city)}
                >
                  📍 {city}
                </div>
              ))
            ) : (
              <div className="no-results">No cities found</div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
