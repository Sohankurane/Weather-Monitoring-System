export const API_ENDPOINTS = {
  CURRENT_WEATHER: '/api/weather/current',
  DASHBOARD: '/api/weather/dashboard',
  ALERTS: '/api/weather/alerts',
  FETCH_NOW: '/api/weather/fetch-now',
};

export const ALERT_TYPES = {
  high_temperature: {
    label: 'High Temperature',
    color: '#ef4444',
    icon: '🌡️'
  },
  high_humidity: {
    label: 'High Humidity',
    color: '#3b82f6',
    icon: '💧'
  },
  extreme_weather: {
    label: 'Extreme Weather',
    color: '#f59e0b',
    icon: '⚠️'
  }
};

export const WEATHER_ICONS = {
  Clear: '☀️',
  Clouds: '☁️',
  Rain: '🌧️',
  Drizzle: '🌦️',
  Thunderstorm: '⛈️',
  Snow: '❄️',
  Mist: '🌫️',
  Fog: '🌫️',
  Haze: '🌫️',
};

export const REFRESH_INTERVAL = 300000; // 5 minutes
