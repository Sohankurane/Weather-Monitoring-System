import React from 'react';
import './ForecastCard.css';

export const ForecastCard = () => {
  // 5-day forecast data
  const forecast = [
    { day: 'Mon', temp: 28, icon: '☀️', condition: 'Sunny' },
    { day: 'Tue', temp: 26, icon: '🌤️', condition: 'Partly Cloudy' },
    { day: 'Wed', temp: 24, icon: '🌧️', condition: 'Rainy' },
    { day: 'Thu', temp: 27, icon: '⛅', condition: 'Cloudy' },
    { day: 'Fri', temp: 29, icon: '☀️', condition: 'Sunny' },
  ];

  return (
    <div className="forecast-container">
      <h3>📅 5-Day Forecast</h3>
      <div className="forecast-grid">
        {forecast.map((day, index) => (
          <div key={index} className="forecast-day">
            <span className="day-name">{day.day}</span>
            <span className="forecast-icon">{day.icon}</span>
            <span className="forecast-temp">{day.temp}°C</span>
            <span className="forecast-condition">{day.condition}</span>
          </div>
        ))}
      </div>
    </div>
  );
};
