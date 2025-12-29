from flask import Blueprint, render_template, request, jsonify, current_app
from .pipeline import StableDiffusionGenerator
from .utils import pil_to_dataurl
import logging
import traceback

logger = logging.getLogger(__name__)

main_bp = Blueprint("main", __name__)

# Global error flag
_pipeline_loaded = False
_pipeline_error = None

@main_bp.before_app_request
def load_pipe():
    """Load the Stable Diffusion pipeline before first request"""
    global _pipeline_loaded, _pipeline_error
    
    if _pipeline_loaded:
        return
    
    try:
        cfg = current_app.config
        logger.info("Initializing Stable Diffusion pipeline...")
        
        current_app.sdgen = StableDiffusionGenerator(
            cfg["MODEL_ID"],
            cfg["DEVICE"],
            cfg["HF_TOKEN"]
        )
        
        _pipeline_loaded = True
        logger.info("Pipeline loaded and ready")
        
    except Exception as e:
        _pipeline_error = str(e)
        logger.error(f"Failed to load pipeline: {e}")
        logger.error(traceback.format_exc())

@main_bp.route("/")
def index():
    """Render the main page"""
    return render_template("index.html")

@main_bp.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    if _pipeline_loaded:
        return jsonify({
            "status": "healthy",
            "pipeline_loaded": True,
            "device_info": current_app.sdgen.get_device_info()
        }), 200
    else:
        return jsonify({
            "status": "unhealthy",
            "pipeline_loaded": False,
            "error": _pipeline_error
        }), 503

@main_bp.route("/generate", methods=["POST"])
def generate():
    """Generate an image from a text prompt"""
    
    # Check if pipeline is loaded
    if not _pipeline_loaded:
        logger.error("Generate called but pipeline not loaded")
        return jsonify({
            "error": "Model not loaded yet. Please wait or check server logs.",
            "details": _pipeline_error
        }), 503
    
    try:
        # Get request data
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        # Validate prompt
        prompt = data.get("prompt", "").strip()
        if not prompt:
            return jsonify({"error": "Prompt is required and cannot be empty"}), 400
        
        # Check prompt length
        max_length = current_app.config.get("MAX_PROMPT_LENGTH", 500)
        if len(prompt) > max_length:
            return jsonify({
                "error": f"Prompt too long. Maximum {max_length} characters allowed."
            }), 400
        
        # Get optional parameters
        cfg = current_app.config
        num_steps = data.get("num_inference_steps", cfg["NUM_INFERENCE_STEPS"])
        guidance = data.get("guidance_scale", cfg["GUIDANCE_SCALE"])
        height = data.get("height", cfg["HEIGHT"])
        width = data.get("width", cfg["WIDTH"])
        seed = data.get("seed")
        
        logger.info(f"Generating image for prompt: {prompt[:50]}...")
        
        # Generate the image
        image = current_app.sdgen.generate(
            prompt=prompt,
            num_inference_steps=num_steps,
            guidance_scale=guidance,
            height=height,
            width=width,
            seed=seed
        )
        
        # Convert to data URL
        image_data = pil_to_dataurl(image)
        
        logger.info("Image generation successful")
        
        return jsonify({
            "success": True,
            "image": image_data,
            "prompt": prompt,
            "parameters": {
                "steps": num_steps,
                "guidance": guidance,
                "height": height,
                "width": width,
                "seed": seed
            }
        }), 200
    
    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        return jsonify({"error": str(e)}), 400
    
    except RuntimeError as e:
        logger.error(f"Runtime error during generation: {e}")
        return jsonify({"error": str(e)}), 500
    
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        logger.error(traceback.format_exc())
        return jsonify({
            "error": "An unexpected error occurred during image generation",
            "details": str(e)
        }), 500

@main_bp.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return jsonify({"error": "Endpoint not found"}), 404

@main_bp.errorhandler(500)
def internal_error(e):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {e}")
    return jsonify({"error": "Internal server error"}), 500
