import base64
import io
from PIL import Image
import logging

logger = logging.getLogger(__name__)

def pil_to_dataurl(img, fmt="PNG"):
    """
    Convert a PIL Image to a data URL for embedding in HTML/JSON
    
    Args:
        img: PIL Image object
        fmt: Image format (PNG, JPEG, etc.)
    
    Returns:
        Data URL string
    """
    try:
        if not isinstance(img, Image.Image):
            raise TypeError("Input must be a PIL Image object")
        
        # Create BytesIO buffer
        buf = io.BytesIO()
        
        # Save image to buffer
        img.save(buf, format=fmt, quality=95)
        
        # Get bytes and encode to base64
        img_bytes = buf.getvalue()
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')
        
        # Create data URL
        mime_type = f"image/{fmt.lower()}"
        data_url = f"data:{mime_type};base64,{img_base64}"
        
        logger.debug(f"Converted image to data URL ({len(img_base64)} bytes)")
        return data_url
        
    except Exception as e:
        logger.error(f"Error converting image to data URL: {e}")
        raise RuntimeError(f"Failed to convert image: {e}")

def validate_image_dimensions(height, width):
    """
    Validate that image dimensions are appropriate for Stable Diffusion
    
    Args:
        height: Image height in pixels
        width: Image width in pixels
    
    Returns:
        Tuple of (validated_height, validated_width)
    """
    try:
        height = int(height)
        width = int(width)
        
        # Clamp to reasonable values
        height = max(256, min(1024, height))
        width = max(256, min(1024, width))
        
        # Ensure divisible by 8
        height = (height // 8) * 8
        width = (width // 8) * 8
        
        return height, width
        
    except (ValueError, TypeError) as e:
        logger.error(f"Invalid dimensions: {e}")
        return 512, 512  # Default fallback
