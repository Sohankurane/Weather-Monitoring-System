import { useState, useEffect } from 'react';
import { weatherAPI } from '../../services/api';
import { REFRESH_INTERVAL } from '../../constants';

export const useWeatherCard = () => {
  const [weatherData, setWeatherData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);

  const fetchWeatherData = async () => {
    try {
      setLoading(true);
      const response = await weatherAPI.getCurrentWeather();
      setWeatherData(response.data[0]); // Get latest weather
      setLastUpdated(new Date());
      setError(null);
    } catch (err) {
      setError(err.message);
      console.error('Error fetching weather data:', err);
    } finally {
      setLoading(false);
    }
  };

  const refreshWeather = async () => {
    try {
      await weatherAPI.fetchWeatherNow();
      await fetchWeatherData();
    } catch (err) {
      setError('Failed to refresh weather data');
    }
  };

  useEffect(() => {
    fetchWeatherData();
    
    // Auto-refresh every 5 minutes
    const interval = setInterval(fetchWeatherData, REFRESH_INTERVAL);
    
    return () => clearInterval(interval);
  }, []);

  return {
    weatherData,
    loading,
    error,
    lastUpdated,
    refreshWeather,
  };
};
