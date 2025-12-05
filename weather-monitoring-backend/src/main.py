from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from src.api.routes import weather
from src.cron.scheduler import start_scheduler, shutdown_scheduler
from src.database.connection import engine
from src.database.base import Base
from src.config.settings import settings
from src.config.logging_config import setup_logging
import logging

# Setup logging first
setup_logging()
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for startup and shutdown"""
    # Startup
    logger.info("🚀 Starting Weather Monitoring System...")
    
    # Create database tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("✅ Database tables ready")
    
    # Start scheduler
    start_scheduler()
    logger.info("✅ Cron scheduler started")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down application...")
    shutdown_scheduler()
    await engine.dispose()
    logger.info("✅ Application shutdown complete")

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="Weather Monitoring & Automation System with Cron Jobs",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(weather.router)

# Health check endpoint
@app.get("/")
async def root():
    return {
        "message": "Weather Monitoring System API",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
