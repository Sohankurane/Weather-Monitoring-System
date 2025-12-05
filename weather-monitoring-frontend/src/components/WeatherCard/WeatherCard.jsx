import React from 'react';
import { useWeatherCard } from './WeatherCard.hook';
import { WEATHER_ICONS } from '../../constants';
import './WeatherCard.css';

export const WeatherCard = () => {
  const { weatherData, loading, error, lastUpdated, refreshWeather } = useWeatherCard();

  if (loading && !weatherData) {
    return (
      <div className="weather-card loading">
        <div className="spinner"></div>
        <p>Loading weather data...</p>
      </div>
    );
  }

  if (error && !weatherData) {
    return (
      <div className="weather-card error">
        <p>❌ Error: {error}</p>
        <button onClick={refreshWeather}>Retry</button>
      </div>
    );
  }

  if (!weatherData) return null;

  const weatherIcon = WEATHER_ICONS[weatherData.weather_main] || '🌍';

  return (
    <div className="weather-card">
      <div className="weather-header">
        <h2>{weatherData.city}</h2>
        <button className="refresh-btn" onClick={refreshWeather} title="Refresh">
          🔄
        </button>
      </div>

      <div className="weather-main">
        <div className="weather-icon">{weatherIcon}</div>
        <div className="temperature">
          <span className="temp-value">{Math.round(weatherData.temperature)}</span>
          <span className="temp-unit">°C</span>
        </div>
        <p className="weather-description">{weatherData.weather_description}</p>
      </div>

      <div className="weather-details">
        <div className="detail-item">
          <span className="detail-label">Feels Like</span>
          <span className="detail-value">{Math.round(weatherData.feels_like)}°C</span>
        </div>
        <div className="detail-item">
          <span className="detail-label">Humidity</span>
          <span className="detail-value">{weatherData.humidity}%</span>
        </div>
        <div className="detail-item">
          <span className="detail-label">Wind Speed</span>
          <span className="detail-value">{weatherData.wind_speed} m/s</span>
        </div>
        <div className="detail-item">
          <span className="detail-label">Pressure</span>
          <span className="detail-value">{weatherData.pressure} hPa</span>
        </div>
      </div>

      {lastUpdated && (
        <div className="last-updated">
          Last updated: {lastUpdated.toLocaleTimeString()}
        </div>
      )}
    </div>
  );
};
