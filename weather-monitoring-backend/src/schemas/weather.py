from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Any

class WeatherDataResponse(BaseModel):
    id: int
    city: str
    temperature: float
    feels_like: float
    temp_min: float
    temp_max: float
    humidity: int
    pressure: int
    weather_main: str
    weather_description: str
    wind_speed: float
    clouds: int
    recorded_at: datetime
    
    class Config:
        from_attributes = True

class DashboardSummaryResponse(BaseModel):
    id: int
    city: str
    avg_temperature: float
    max_temperature: float
    min_temperature: float
    avg_humidity: float
    trend_data: Dict[str, Any]
    computed_at: datetime
    
    class Config:
        from_attributes = True

class WeatherAlertResponse(BaseModel):
    id: int
    city: str
    alert_type: str
    message: str
    threshold_value: Optional[float]
    actual_value: float
    created_at: datetime
    is_sent: bool
    
    class Config:
        from_attributes = True

class AlertThreshold(BaseModel):
    high_temperature: float = Field(default=35.0, description="Temperature in Celsius")
    high_humidity: int = Field(default=80, description="Humidity percentage")
    extreme_weather_conditions: list[str] = Field(
        default=["Thunderstorm", "Heavy Rain", "Storm", "Tornado", "Hurricane"]
    )
