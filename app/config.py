import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class Config:
    """Application configuration with validation and error handling"""
    
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
    HF_TOKEN = os.environ.get("HF_TOKEN")
    
    # Device configuration with fallback
    DEVICE = os.environ.get("DEVICE", "cpu")  # Default to CPU if not specified
    
    # Model configuration
    MODEL_ID = os.environ.get("MODEL_ID", "runwayml/stable-diffusion-v1-5")
    
    # Generation parameters with validation
    try:
        NUM_INFERENCE_STEPS = int(os.environ.get("NUM_INFERENCE_STEPS", 28))
        if NUM_INFERENCE_STEPS < 1 or NUM_INFERENCE_STEPS > 100:
            NUM_INFERENCE_STEPS = 28
    except ValueError:
        NUM_INFERENCE_STEPS = 28
    
    try:
        GUIDANCE_SCALE = float(os.environ.get("GUIDANCE_SCALE", 7.5))
        if GUIDANCE_SCALE < 0 or GUIDANCE_SCALE > 20:
            GUIDANCE_SCALE = 7.5
    except ValueError:
        GUIDANCE_SCALE = 7.5
    
    try:
        HEIGHT = int(os.environ.get("HEIGHT", 512))
        if HEIGHT < 256 or HEIGHT > 1024 or HEIGHT % 8 != 0:
            HEIGHT = 512
    except ValueError:
        HEIGHT = 512
    
    try:
        WIDTH = int(os.environ.get("WIDTH", 512))
        if WIDTH < 256 or WIDTH > 1024 or WIDTH % 8 != 0:
            WIDTH = 512
    except ValueError:
        WIDTH = 512
    
    # Request limits
    MAX_PROMPT_LENGTH = 500
    REQUEST_TIMEOUT = 120  # seconds
    
    # Logging
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
