from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.connection import get_db
from src.services.weather_service import WeatherService
from src.services.alert_service import AlertService
from src.schemas.weather import (
    WeatherDataResponse, 
    DashboardSummaryResponse,
    WeatherAlertResponse
)
from typing import List
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/weather", tags=["weather"])


@router.get("/current", response_model=List[WeatherDataResponse])
async def get_current_weather(db: AsyncSession = Depends(get_db)):
    """Get latest weather data"""
    try:
        weather_data = await WeatherService.get_latest_weather(db)
        if not weather_data:
            raise HTTPException(status_code=404, detail="No weather data found")
        return weather_data
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching current weather: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dashboard", response_model=DashboardSummaryResponse)
async def get_dashboard_summary(db: AsyncSession = Depends(get_db)):
    """Get dashboard summary data"""
    try:
        summary = await WeatherService.get_dashboard_summary(db)
        if not summary:
            
            logger.info("No dashboard summary found, computing new summary...")
            summary = await WeatherService.compute_dashboard_summary(db)
            if not summary:
                raise HTTPException(
                    status_code=404, 
                    detail="No weather data available to create summary. Please fetch weather data first."
                )
        return summary
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching dashboard summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/alerts", response_model=List[WeatherAlertResponse])
async def get_alerts(db: AsyncSession = Depends(get_db)):
    """Get recent weather alerts"""
    try:
        alerts = await AlertService.get_recent_alerts(db)
        return alerts
    except Exception as e:
        logger.error(f"Error fetching alerts: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/fetch-now")
async def fetch_weather_now(db: AsyncSession = Depends(get_db)):
    """Manually trigger weather data fetch"""
    try:
        logger.info("Manual weather fetch triggered...")
        weather_data = await WeatherService.fetch_weather_from_api()
        saved_data = await WeatherService.save_weather_data(db, weather_data)
        return {
            "message": "Weather data fetched successfully", 
            "data": {
                "id": saved_data.id,
                "city": saved_data.city,
                "temperature": saved_data.temperature,
                "humidity": saved_data.humidity,
                "weather": saved_data.weather_main,
                "recorded_at": saved_data.recorded_at
            }
        }
    except Exception as e:
        logger.error(f"Error fetching weather data: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch weather data: {str(e)}")


@router.post("/compute-summary")
async def compute_summary_now(db: AsyncSession = Depends(get_db)):
    """Manually trigger dashboard summary computation"""
    try:
        logger.info("Manual dashboard summary computation triggered...")
        summary = await WeatherService.compute_dashboard_summary(db)
        if not summary:
            raise HTTPException(
                status_code=404, 
                detail="No weather data available. Please fetch weather data first."
            )
        return {
            "message": "Dashboard summary computed successfully", 
            "data": {
                "id": summary.id,
                "city": summary.city,
                "avg_temperature": summary.avg_temperature,
                "max_temperature": summary.max_temperature,
                "min_temperature": summary.min_temperature,
                "avg_humidity": summary.avg_humidity,
                "computed_at": summary.computed_at
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error computing dashboard summary: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to compute summary: {str(e)}")


@router.post("/trigger-alert-check")
async def trigger_alert_check(db: AsyncSession = Depends(get_db)):
    """Manually trigger weather alert check"""
    try:
        logger.info("Manual alert check triggered...")
        from src.schemas.weather import AlertThreshold
        thresholds = AlertThreshold()
        alerts = await AlertService.check_weather_alerts(db, thresholds)
        return {
            "message": f"Alert check completed. {len(alerts)} alerts created.",
            "alerts_count": len(alerts),
            "alerts": [
                {
                    "id": alert.id,
                    "type": alert.alert_type,
                    "message": alert.message,
                    "created_at": alert.created_at
                }
                for alert in alerts
            ]
        }
    except Exception as e:
        logger.error(f"Error checking alerts: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to check alerts: {str(e)}")


@router.delete("/cleanup-data")
async def cleanup_old_data(db: AsyncSession = Depends(get_db), days: int = 2, hard_delete: bool = False):
    """Manually trigger data cleanup (for testing purposes)"""
    try:
        logger.info(f"Manual data cleanup triggered (days={days}, hard_delete={hard_delete})...")
        deleted_count = await WeatherService.cleanup_old_data(db, days=days, hard_delete=hard_delete)
        return {
            "message": "Data cleanup completed successfully",
            "deleted_count": deleted_count,
            "cleanup_type": "hard_delete" if hard_delete else "soft_delete"
        }
    except Exception as e:
        logger.error(f"Error during data cleanup: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to cleanup data: {str(e)}")
