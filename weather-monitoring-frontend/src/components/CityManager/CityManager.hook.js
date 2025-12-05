import { useState, useEffect } from 'react';

export const useCityManager = () => {
  const [cities, setCities] = useState(['Pune', 'Mumbai', 'Delhi']);

  // Load cities from localStorage on mount
  useEffect(() => {
    const savedCities = localStorage.getItem('weather_cities');
    if (savedCities) {
      setCities(JSON.parse(savedCities));
    }
  }, []);

  // Save cities to localStorage whenever they change
  useEffect(() => {
    localStorage.setItem('weather_cities', JSON.stringify(cities));
  }, [cities]);

  const addCity = (city) => {
    if (!cities.includes(city) && cities.length < 5) {
      setCities([...cities, city]);
    }
  };

  const removeCity = (cityToRemove) => {
    if (cities.length > 1) {
      setCities(cities.filter(city => city !== cityToRemove));
    } else {
      alert('At least one city must be selected!');
    }
  };

  return {
    cities,
    addCity,
    removeCity,
  };
};
