from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, JSON
from sqlalchemy.sql import func
from src.database.base import Base

class WeatherData(Base):
    __tablename__ = "weather_data"
    
    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, index=True)
    temperature = Column(Float)
    feels_like = Column(Float)
    temp_min = Column(Float)
    temp_max = Column(Float)
    humidity = Column(Integer)
    pressure = Column(Integer)
    weather_main = Column(String)
    weather_description = Column(String)
    wind_speed = Column(Float)
    clouds = Column(Integer)
    recorded_at = Column(DateTime(timezone=True), server_default=func.now())
    is_deleted = Column(Boolean, default=False)  # For soft delete
    
class DashboardSummary(Base):
    __tablename__ = "dashboard_summary"
    
    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, index=True)
    avg_temperature = Column(Float)
    max_temperature = Column(Float)
    min_temperature = Column(Float)
    avg_humidity = Column(Float)
    trend_data = Column(JSON)  # Store hourly trends
    computed_at = Column(DateTime(timezone=True), server_default=func.now())

class WeatherAlert(Base):
    __tablename__ = "weather_alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, index=True)
    alert_type = Column(String)  # high_temp, high_humidity, extreme_weather
    message = Column(String)
    threshold_value = Column(Float, nullable=True)
    actual_value = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_sent = Column(Boolean, default=False)
