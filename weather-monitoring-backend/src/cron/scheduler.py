from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from src.database.connection import AsyncSessionLocal
from src.services.weather_service import WeatherService
from src.services.alert_service import AlertService
from src.schemas.weather import AlertThreshold
import logging

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()

# Job 1: Fetch weather data every 30 minutes
async def fetch_weather_job():
    """Cron job to fetch weather data from OpenWeatherMap API"""
    logger.info("⏰ Fetching weather data...")
    async with AsyncSessionLocal() as db:
        try:
            weather_data = await WeatherService.fetch_weather_from_api()
            await WeatherService.save_weather_data(db, weather_data)
            logger.info(f"✅ Weather data saved: {weather_data['name']} - {weather_data['main']['temp']}°C")
        except Exception as e:
            logger.error(f"❌ Weather fetch failed: {e}")

# Job 2: Compute dashboard summary every hour
async def dashboard_summary_job():
    """Cron job to compute dashboard summary data"""
    logger.info("⏰ Computing dashboard summary...")
    async with AsyncSessionLocal() as db:
        try:
            summary = await WeatherService.compute_dashboard_summary(db)
            if summary:
                logger.info(f"✅ Dashboard summary computed: Avg {summary.avg_temperature}°C")
            else:
                logger.warning("⚠️ No data for dashboard summary")
        except Exception as e:
            logger.error(f"❌ Dashboard summary failed: {e}")

# Job 3: Cleanup old data daily
async def cleanup_data_job():
    """Cron job to cleanup old weather records"""
    logger.info("⏰ Cleaning up old data...")
    async with AsyncSessionLocal() as db:
        try:
            deleted_count = await WeatherService.cleanup_old_data(db, days=2, hard_delete=False)
            logger.info(f"✅ Cleaned {deleted_count} old records")
        except Exception as e:
            logger.error(f"❌ Data cleanup failed: {e}")

# Job 4: Check weather alerts every 15 minutes
async def weather_alert_job():
    """Cron job to check weather conditions and send alerts"""
    logger.info("⏰ Checking weather alerts...")
    async with AsyncSessionLocal() as db:
        try:
            thresholds = AlertThreshold(
                high_temperature=35.0,
                high_humidity=80,
                extreme_weather_conditions=["Thunderstorm", "Heavy Rain", "Storm", "Tornado", "Hurricane"]
            )
            
            alerts = await AlertService.check_weather_alerts(db, thresholds)
            if alerts:
                logger.warning(f"⚠️ {len(alerts)} weather alerts triggered!")
                for alert in alerts:
                    logger.warning(f"🚨 {alert.alert_type.upper()}: {alert.message}")
            else:
                logger.info("✅ No alerts - conditions normal")
        except Exception as e:
            logger.error(f"❌ Alert check failed: {e}")

def start_scheduler():
    """Initialize and start all cron jobs"""
    
    # Job 1: Fetch weather every 30 minutes
    scheduler.add_job(
        fetch_weather_job,
        trigger=CronTrigger(minute="*/30"),
        id="fetch_weather_job",
        name="Fetch weather data",
        replace_existing=True
    )
    
    # Job 2: Compute dashboard summary every hour
    scheduler.add_job(
        dashboard_summary_job,
        trigger=CronTrigger(minute="0"),
        id="dashboard_summary_job",
        name="Dashboard summary",
        replace_existing=True
    )
    
    # Job 3: Cleanup data daily at midnight
    scheduler.add_job(
        cleanup_data_job,
        trigger=CronTrigger(hour="0", minute="0"),
        id="cleanup_data_job",
        name="Data cleanup",
        replace_existing=True
    )
    
    # Job 4: Check alerts every 15 minutes
    scheduler.add_job(
        weather_alert_job,
        trigger=CronTrigger(minute="*/15"),
        id="weather_alert_job",
        name="Weather alerts",
        replace_existing=True
    )
    
    scheduler.start()
    logger.info("📅 All cron jobs scheduled successfully")

def shutdown_scheduler():
    """Shutdown the scheduler gracefully"""
    if scheduler.running:
        scheduler.shutdown()
        logger.info("📅 Scheduler stopped")
