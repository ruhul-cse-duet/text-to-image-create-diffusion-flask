import torch
from diffusers import DiffusionPipeline
from PIL import Image
from contextlib import nullcontext
import logging

logger = logging.getLogger(__name__)

class StableDiffusionGenerator:
    """Stable Diffusion image generator with comprehensive error handling"""
    
    def __init__(self, model_id, device="cuda", hf_token=None):
        """
        Initialize the Stable Diffusion pipeline
        
        Args:
            model_id: HuggingFace model identifier
            device: Device to run on ('cuda' or 'cpu')
            hf_token: HuggingFace authentication token
        """
        self.model_id = model_id
        self.hf_token = hf_token
        self.pipe = None
        
        # Validate and set device
        try:
            if device and device.startswith("cuda") and torch.cuda.is_available():
                self.device = torch.device(device)
                logger.info(f"Using GPU: {torch.cuda.get_device_name(0)}")
            else:
                self.device = torch.device("cpu")
                if not torch.cuda.is_available():
                    logger.warning("CUDA not available, using CPU (this will be slower)")
                else:
                    logger.info("Using CPU as requested")
        except Exception as e:
            logger.error(f"Error setting device: {e}, defaulting to CPU")
            self.device = torch.device("cpu")
        
        # Load the pipeline
        self._load_pipeline()
    
    def _load_pipeline(self):
        """Load the Stable Diffusion pipeline with error handling"""
        try:
            logger.info(f"Loading model: {self.model_id}")
            
            # Set up kwargs based on device
            kwargs = {}
            if self.device.type == "cuda":
                kwargs["torch_dtype"] = torch.float16
            
            if self.hf_token:
                kwargs["use_auth_token"] = self.hf_token
            
            # Load the pipeline
            self.pipe = DiffusionPipeline.from_pretrained(
                self.model_id,
                safety_checker=None,
                low_cpu_mem_usage=False,  # Explicitly disable to avoid accelerate requirement issues
                **kwargs
            )
            
            # Move to device
            self.pipe = self.pipe.to(self.device)
            logger.info("Pipeline loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load pipeline: {e}")
            raise RuntimeError(f"Could not load Stable Diffusion model: {e}")
    
    def generate(self, prompt, num_inference_steps=28, guidance_scale=7.5, 
                 height=512, width=512, seed=None):
        """
        Generate an image from a text prompt
        
        Args:
            prompt: Text description of the image to generate
            num_inference_steps: Number of denoising steps (more = better quality but slower)
            guidance_scale: How closely to follow the prompt (higher = more literal)
            height: Image height in pixels (must be divisible by 8)
            width: Image width in pixels (must be divisible by 8)
            seed: Random seed for reproducibility
            
        Returns:
            PIL Image object
        """
        if not self.pipe:
            raise RuntimeError("Pipeline not loaded. Cannot generate image.")
        
        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty")
        
        try:
            # Validate parameters
            num_inference_steps = max(1, min(100, int(num_inference_steps)))
            guidance_scale = max(0, min(20, float(guidance_scale)))
            height = max(256, min(1024, int(height)))
            width = max(256, min(1024, int(width)))
            
            # Ensure dimensions are divisible by 8
            height = (height // 8) * 8
            width = (width // 8) * 8
            
            logger.info(f"Generating image: {prompt[:50]}... ({height}x{width})")
            
            # Set up random seed if provided
            generator = None
            if seed is not None:
                try:
                    generator = torch.Generator(device=self.device).manual_seed(int(seed))
                    logger.info(f"Using seed: {seed}")
                except Exception as e:
                    logger.warning(f"Invalid seed {seed}, using random generation: {e}")
            
            # Use autocast for CUDA to improve performance
            context_manager = torch.autocast(self.device.type) if self.device.type == "cuda" else nullcontext()
            
            with context_manager:
                output = self.pipe(
                    prompt,
                    height=height,
                    width=width,
                    num_inference_steps=num_inference_steps,
                    guidance_scale=guidance_scale,
                    generator=generator
                )
            
            logger.info("Image generated successfully")
            return output.images[0]
            
        except torch.cuda.OutOfMemoryError:
            logger.error("GPU out of memory")
            raise RuntimeError("GPU out of memory. Try reducing image size or using CPU.")
        except Exception as e:
            logger.error(f"Error during image generation: {e}")
            raise RuntimeError(f"Failed to generate image: {str(e)}")
    
    def get_device_info(self):
        """Get information about the current device"""
        info = {
            "device": str(self.device),
            "device_type": self.device.type
        }
        
        if self.device.type == "cuda":
            info.update({
                "gpu_name": torch.cuda.get_device_name(0),
                "gpu_memory_allocated": f"{torch.cuda.memory_allocated(0) / 1024**3:.2f} GB",
                "gpu_memory_reserved": f"{torch.cuda.memory_reserved(0) / 1024**3:.2f} GB"
            })
        
        return info
