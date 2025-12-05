# 🌤️ Weather Monitoring & Automation System

A full-stack weather monitoring application with automated cron jobs, real-time weather data, and intelligent alerting system.

## 🚀 Features

### Backend (FastAPI + PostgreSQL)
- ✅ **Weather Data Fetching** - Automated weather data collection every 30 minutes
- ✅ **Dashboard Analytics** - Hourly computation of trends, averages, and metrics
- ✅ **Data Cleanup** - Daily maintenance of weather records
- ✅ **Smart Alerts** - 15-minute interval checks for weather thresholds
- ✅ **RESTful API** - Complete API for frontend integration
- ✅ **PostgreSQL Database** - Reliable data storage with SQLAlchemy ORM

### Frontend (React + Vite)
- ✅ **Multi-City Weather** - Monitor up to 5 cities simultaneously
- ✅ **Real-time Dashboard** - Live weather data with auto-refresh
- ✅ **Interactive Charts** - Temperature and humidity trends
- ✅ **Weather Alerts** - Visual alerts for extreme conditions
- ✅ **Dark/Light Theme** - User-friendly theme toggle
- ✅ **5-Day Forecast** - Extended weather predictions
- ✅ **Responsive Design** - Mobile-friendly interface

## 🛠️ Tech Stack

**Backend:**
- Python 3.10+
- FastAPI
- PostgreSQL
- SQLAlchemy (Async)
- APScheduler
- OpenWeatherMap API

**Frontend:**
- React 18
- Vite
- Axios
- Recharts
- CSS3

## 📋 Prerequisites

- Python 3.10 or higher
- Node.js 18 or higher
- PostgreSQL 14 or higher
- OpenWeatherMap API Key

## 🔧 Installation & Setup

### Backend Setup

1. **Navigate to backend directory:**

2. **Create virtual environment:**

3. **Install dependencies:**

4. **Create `.env` file:**
DATABASE_URL=postgresql+asyncpg://postgres:yourpassword@localhost:5432/weather_monitoring
POSTGRES_USER=postgres
POSTGRES_PASSWORD=yourpassword
POSTGRES_DB=weather_monitoring
OPENWEATHER_API_KEY=your_api_key_here
OPENWEATHER_BASE_URL=https://api.openweathermap.org/data/2.5
CITY_NAME=Pune

5. **Create PostgreSQL database:**

6. **Run the backend:**

Backend will be available at: `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory:**

2. **Install dependencies:**

3. **Create `.env` file:**

4. **Run the frontend:**

Frontend will be available at: `http://localhost:3000`

## 📊 Database Schema

### Tables

1. **weather_data** - Stores raw weather data from API
2. **dashboard_summary** - Stores computed trends and metrics
3. **weather_alerts** - Stores alert logs with thresholds

## 🔄 Cron Jobs

| Job | Frequency | Description |
|-----|-----------|-------------|
| Weather Fetch | Every 30 minutes | Fetches data from OpenWeatherMap |
| Dashboard Summary | Every 1 hour | Computes trends and averages |
| Data Cleanup | Daily at midnight | Archives old weather records |
| Weather Alerts | Every 15 minutes | Checks threshold conditions |

## 🌐 API Endpoints

- `GET /` - API health check
- `GET /api/weather/current` - Get latest weather data
- `GET /api/weather/dashboard` - Get dashboard summary
- `GET /api/weather/alerts` - Get weather alerts
- `POST /api/weather/fetch-now` - Manually trigger weather fetch
- `POST /api/weather/compute-summary` - Manually compute summary
- `POST /api/weather/trigger-alert-check` - Manually check alerts

## 📸 Screenshots

Add your screenshots here

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License.

## 👨‍💻 Author

Your Name - Sohan Kurane

## 🙏 Acknowledgments

- OpenWeatherMap API for weather data
- FastAPI documentation
- React community
