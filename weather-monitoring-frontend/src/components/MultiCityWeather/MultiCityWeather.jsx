import React from 'react';
import { useMultiCityWeather } from './MultiCityWeather.hook';
import { WEATHER_ICONS } from '../../constants';
import './MultiCityWeather.css';

export const MultiCityWeather = ({ cities }) => {
  const { weatherData, loading, error } = useMultiCityWeather(cities);

  if (loading && weatherData.length === 0) {
    return <div className="multi-city-loading">Loading weather data...</div>;
  }

  return (
    <div className="multi-city-container">
      {cities.map((city, index) => {
        const cityWeather = weatherData[city];
        
        if (!cityWeather) {
          return (
            <div key={index} className="city-weather-card loading">
              <p>Loading {city}...</p>
            </div>
          );
        }

        const weatherIcon = WEATHER_ICONS[cityWeather.weather_main] || '🌍';

        return (
          <div key={index} className="city-weather-card">
            <div className="city-header">
              <h3>{city}</h3>
              <span className="weather-icon-small">{weatherIcon}</span>
            </div>
            
            <div className="city-temp">
              <span className="temp-large">{Math.round(cityWeather.temperature)}</span>
              <span className="temp-unit-small">°C</span>
            </div>
            
            <p className="city-condition">{cityWeather.weather_description}</p>
            
            <div className="city-details-grid">
              <div className="detail-mini">
                <span className="label">Humidity</span>
                <span className="value">{cityWeather.humidity}%</span>
              </div>
              <div className="detail-mini">
                <span className="label">Wind</span>
                <span className="value">{cityWeather.wind_speed} m/s</span>
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
};
