import { useState, useEffect } from 'react';
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
const OPENWEATHER_API_KEY = import.meta.env.VITE_OPENWEATHER_API_KEY;
const OPENWEATHER_BASE_URL = 'https://api.openweathermap.org/data/2.5';

export const useMultiCityWeather = (cities) => {
  const [weatherData, setWeatherData] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchWeatherForCities = async () => {
      setLoading(true);
      const newWeatherData = {};

      try {
        // Fetch weather for each city
        const promises = cities.map(async (city) => {
          try {
            const response = await axios.get(`${OPENWEATHER_BASE_URL}/weather`, {
              params: {
                q: city,
                appid: OPENWEATHER_API_KEY,
                units: 'metric'
              }
            });

            return {
              city,
              data: {
                temperature: response.data.main.temp,
                feels_like: response.data.main.feels_like,
                humidity: response.data.main.humidity,
                pressure: response.data.main.pressure,
                weather_main: response.data.weather[0].main,
                weather_description: response.data.weather[0].description,
                wind_speed: response.data.wind.speed,
                clouds: response.data.clouds.all,
              }
            };
          } catch (err) {
            console.error(`Error fetching weather for ${city}:`, err);
            return null;
          }
        });

        const results = await Promise.all(promises);
        
        results.forEach(result => {
          if (result) {
            newWeatherData[result.city] = result.data;
          }
        });

        setWeatherData(newWeatherData);
        setError(null);
      } catch (err) {
        setError(err.message);
        console.error('Error fetching multi-city weather:', err);
      } finally {
        setLoading(false);
      }
    };

    if (cities.length > 0) {
      fetchWeatherForCities();
    }
  }, [cities]);

  return {
    weatherData,
    loading,
    error,
  };
};
