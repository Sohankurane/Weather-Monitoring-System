import React from 'react';
import { useDashboard } from './Dashboard.hook';
import { useCityManager } from '../CityManager/CityManager.hook';
import { WeatherCard } from '../WeatherCard/WeatherCard';
import { AlertsList } from '../AlertsList/AlertsList';
import { WeatherChart } from '../WeatherChart/WeatherChart';
import { ForecastCard } from '../ForecastCard/ForecastCard';
import { ThemeToggle } from '../ThemeToggle/ThemeToggle';
import { CityManager } from '../CityManager/CityManager';
import { MultiCityWeather } from '../MultiCityWeather/MultiCityWeather';
import './Dashboard.css';

export const Dashboard = () => {
  const { dashboardData, loading, error } = useDashboard();
  const { cities, addCity, removeCity } = useCityManager();

  return (
    <div className="dashboard-container">
      {/* Theme Toggle Button */}
      <ThemeToggle />

      <header className="dashboard-header">
        <h1>🌤️ Weather Monitoring System</h1>
        <p className="subtitle">Real-time weather data across multiple cities</p>
        
        {/* City Manager */}
        <CityManager 
          cities={cities}
          onAddCity={addCity}
          onRemoveCity={removeCity}
        />
      </header>

      {/* Multi-City Weather Cards */}
      <MultiCityWeather cities={cities} />

      <div className="dashboard-grid">
        {/* Current Weather Card for Pune */}
        <div className="grid-item">
          <WeatherCard />
        </div>

        {/* Summary Statistics */}
        <div className="grid-item">
          <div className="summary-card">
            <h3>📊 Today's Summary (Pune)</h3>
            {loading && !dashboardData && (
              <div className="loading-state">Loading summary...</div>
            )}
            {error && !dashboardData && (
              <div className="error-state">Failed to load summary</div>
            )}
            {dashboardData && (
              <div className="summary-stats">
                <div className="stat-item">
                  <span className="stat-icon">📈</span>
                  <div className="stat-info">
                    <span className="stat-label">Max Temperature</span>
                    <span className="stat-value">
                      {Math.round(dashboardData.max_temperature)}°C
                    </span>
                  </div>
                </div>
                <div className="stat-item">
                  <span className="stat-icon">📉</span>
                  <div className="stat-info">
                    <span className="stat-label">Min Temperature</span>
                    <span className="stat-value">
                      {Math.round(dashboardData.min_temperature)}°C
                    </span>
                  </div>
                </div>
                <div className="stat-item">
                  <span className="stat-icon">🌡️</span>
                  <div className="stat-info">
                    <span className="stat-label">Avg Temperature</span>
                    <span className="stat-value">
                      {Math.round(dashboardData.avg_temperature)}°C
                    </span>
                  </div>
                </div>
                <div className="stat-item">
                  <span className="stat-icon">💧</span>
                  <div className="stat-info">
                    <span className="stat-label">Avg Humidity</span>
                    <span className="stat-value">
                      {Math.round(dashboardData.avg_humidity)}%
                    </span>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* 5-Day Forecast */}
        <div className="grid-item forecast-item">
          <ForecastCard />
        </div>

        {/* Temperature Trend Chart */}
        <div className="grid-item chart-section">
          <WeatherChart data={dashboardData} />
        </div>

        {/* Weather Alerts */}
        <div className="grid-item alerts-section">
          <AlertsList />
        </div>
      </div>
    </div>
  );
};
