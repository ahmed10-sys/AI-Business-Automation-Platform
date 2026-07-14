import logging
import uvicorn
from fastapi import FastAPI
from app.config import settings
from app.api.webhook import router as webhook_router

# Setup logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("whatsapp_engine")

app = FastAPI(
    title="WhatsApp Business Automation Engine",
    description="Core backend engine for WhatsApp automation, webhooks, and routing.",
    version="1.0.0"
)

# Register routes
app.include_router(webhook_router)

@app.get("/", tags=["General"])
async def root():
    """
    Root endpoint for service verification and basic status.
    """
    return {
        "service": "WhatsApp Business Automation Engine",
        "status": "online",
        "version": "1.0.0"
    }

@app.get("/health", tags=["General"])
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    )