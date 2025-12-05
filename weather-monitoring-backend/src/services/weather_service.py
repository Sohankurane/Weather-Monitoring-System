import httpx
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, and_, func
from src.models.weather import WeatherData, DashboardSummary
from src.config.settings import settings
import logging

logger = logging.getLogger(__name__)

class WeatherService:
    
    @staticmethod
    async def fetch_weather_from_api(city: str = settings.CITY_NAME) -> dict:
        """Fetch weather data from OpenWeatherMap API"""
        try:
            url = f"{settings.OPENWEATHER_BASE_URL}/weather"
            params = {
                "q": city,
                "appid": settings.OPENWEATHER_API_KEY,
                "units": "metric"  # Get temperature in Celsius
            }
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Error fetching weather data: {e}")
            raise
    
    @staticmethod
    async def save_weather_data(db: AsyncSession, weather_data: dict) -> WeatherData:
        """Save weather data to database"""
        try:
            db_weather = WeatherData(
                city=weather_data["name"],
                temperature=weather_data["main"]["temp"],
                feels_like=weather_data["main"]["feels_like"],
                temp_min=weather_data["main"]["temp_min"],
                temp_max=weather_data["main"]["temp_max"],
                humidity=weather_data["main"]["humidity"],
                pressure=weather_data["main"]["pressure"],
                weather_main=weather_data["weather"][0]["main"],
                weather_description=weather_data["weather"][0]["description"],
                wind_speed=weather_data["wind"]["speed"],
                clouds=weather_data["clouds"]["all"],
                is_deleted=False
            )
            
            db.add(db_weather)
            await db.commit()
            await db.refresh(db_weather)
            return db_weather
        except Exception as e:
            await db.rollback()
            logger.error(f"Error saving weather data: {e}")
            raise
    
    @staticmethod
    async def get_latest_weather(db: AsyncSession, city: str = settings.CITY_NAME):
        """Get latest weather data for a city"""
        query = select(WeatherData).where(
            and_(
                WeatherData.city == city,
                WeatherData.is_deleted == False
            )
        ).order_by(WeatherData.recorded_at.desc()).limit(10)
        
        result = await db.execute(query)
        return result.scalars().all()
    
    @staticmethod
    async def compute_dashboard_summary(db: AsyncSession, city: str = settings.CITY_NAME):
        """Compute summary data for dashboard"""
        try:
            # Get weather data from last 24 hours
            one_hour_ago = datetime.utcnow() - timedelta(hours=24)
            
            query = select(WeatherData).where(
                and_(
                    WeatherData.city == city,
                    WeatherData.recorded_at >= one_hour_ago,
                    WeatherData.is_deleted == False
                )
            )
            
            result = await db.execute(query)
            weather_records = result.scalars().all()
            
            if not weather_records:
                logger.warning("No weather records found for dashboard summary")
                return None
            
            # Calculate averages
            avg_temp = sum(w.temperature for w in weather_records) / len(weather_records)
            max_temp = max(w.temperature for w in weather_records)
            min_temp = min(w.temperature for w in weather_records)
            avg_humidity = sum(w.humidity for w in weather_records) / len(weather_records)
            
            # Create trend data (hourly)
            trend_data = {
                "hourly_temps": [
                    {
                        "time": w.recorded_at.isoformat(),
                        "temperature": w.temperature,
                        "humidity": w.humidity
                    }
                    for w in weather_records[-12:]  # Last 12 records
                ]
            }
            
            # Save summary
            summary = DashboardSummary(
                city=city,
                avg_temperature=round(avg_temp, 2),
                max_temperature=round(max_temp, 2),
                min_temperature=round(min_temp, 2),
                avg_humidity=round(avg_humidity, 2),
                trend_data=trend_data
            )
            
            db.add(summary)
            await db.commit()
            await db.refresh(summary)
            return summary
            
        except Exception as e:
            await db.rollback()
            logger.error(f"Error computing dashboard summary: {e}")
            raise
    
    @staticmethod
    async def cleanup_old_data(db: AsyncSession, days: int = 2, hard_delete: bool = False):
        """Delete or archive weather records older than specified days"""
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            
            if hard_delete:
                # Hard delete
                query = delete(WeatherData).where(
                    WeatherData.recorded_at < cutoff_date
                )
                result = await db.execute(query)
                deleted_count = result.rowcount
            else:
                # Soft delete
                query = select(WeatherData).where(
                    and_(
                        WeatherData.recorded_at < cutoff_date,
                        WeatherData.is_deleted == False
                    )
                )
                result = await db.execute(query)
                records = result.scalars().all()
                
                for record in records:
                    record.is_deleted = True
                
                deleted_count = len(records)
            
            await db.commit()
            logger.info(f"Cleaned up {deleted_count} weather records")
            return deleted_count
            
        except Exception as e:
            await db.rollback()
            logger.error(f"Error during data cleanup: {e}")
            raise
    
    @staticmethod
    async def get_dashboard_summary(db: AsyncSession, city: str = settings.CITY_NAME):
        """Get latest dashboard summary"""
        query = select(DashboardSummary).where(
            DashboardSummary.city == city
        ).order_by(DashboardSummary.computed_at.desc()).limit(1)
        
        result = await db.execute(query)
        return result.scalar_one_or_none()
