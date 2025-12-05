from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from src.models.weather import WeatherData, WeatherAlert
from src.schemas.weather import AlertThreshold
from src.config.settings import settings
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class AlertService:
    
    @staticmethod
    async def check_weather_alerts(db: AsyncSession, thresholds: AlertThreshold = AlertThreshold()):
        """Check weather conditions and create alerts if thresholds are exceeded"""
        try:
            # Get latest weather data
            query = select(WeatherData).where(
                and_(
                    WeatherData.city == settings.CITY_NAME,
                    WeatherData.is_deleted == False
                )
            ).order_by(WeatherData.recorded_at.desc()).limit(1)
            
            result = await db.execute(query)
            latest_weather = result.scalar_one_or_none()
            
            if not latest_weather:
                logger.warning("No weather data found for alert checking")
                return []
            
            alerts = []
            
            # Check high temperature
            if latest_weather.temperature > thresholds.high_temperature:
                alert = WeatherAlert(
                    city=latest_weather.city,
                    alert_type="high_temperature",
                    message=f"High temperature alert! Current: {latest_weather.temperature}°C, Threshold: {thresholds.high_temperature}°C",
                    threshold_value=thresholds.high_temperature,
                    actual_value=latest_weather.temperature,
                    is_sent=False
                )
                alerts.append(alert)
            
            # Check high humidity
            if latest_weather.humidity > thresholds.high_humidity:
                alert = WeatherAlert(
                    city=latest_weather.city,
                    alert_type="high_humidity",
                    message=f"High humidity alert! Current: {latest_weather.humidity}%, Threshold: {thresholds.high_humidity}%",
                    threshold_value=float(thresholds.high_humidity),
                    actual_value=float(latest_weather.humidity),
                    is_sent=False
                )
                alerts.append(alert)
            
            # Check extreme weather
            if latest_weather.weather_main in thresholds.extreme_weather_conditions:
                alert = WeatherAlert(
                    city=latest_weather.city,
                    alert_type="extreme_weather",
                    message=f"Extreme weather alert! Current condition: {latest_weather.weather_main} - {latest_weather.weather_description}",
                    threshold_value=None,
                    actual_value=0.0,
                    is_sent=False
                )
                alerts.append(alert)
            
            # Save alerts
            if alerts:
                db.add_all(alerts)
                await db.commit()
                logger.info(f"Created {len(alerts)} weather alerts")
            
            return alerts
            
        except Exception as e:
            await db.rollback()
            logger.error(f"Error checking weather alerts: {e}")
            raise
    
    @staticmethod
    async def get_recent_alerts(db: AsyncSession, city: str = settings.CITY_NAME, limit: int = 10):
        """Get recent alerts for a city"""
        query = select(WeatherAlert).where(
            WeatherAlert.city == city
        ).order_by(WeatherAlert.created_at.desc()).limit(limit)
        
        result = await db.execute(query)
        return result.scalars().all()
    
    @staticmethod
    async def mark_alert_as_sent(db: AsyncSession, alert_id: int):
        """Mark alert as sent"""
        query = select(WeatherAlert).where(WeatherAlert.id == alert_id)
        result = await db.execute(query)
        alert = result.scalar_one_or_none()
        
        if alert:
            alert.is_sent = True
            await db.commit()
            return alert
        return None
