# 🎨 AI Image Generator - Text to Image with Stable Diffusion

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![Stable Diffusion](https://img.shields.io/badge/Stable%20Diffusion-v1.5-purple)
![License](https://img.shields.io/badge/License-MIT-yellow)

A modern, production-ready Flask web application that transforms text prompts into stunning images using Stable Diffusion AI model. Features a beautiful, responsive UI with advanced customization options.



## ✨ Features

### 🎯 Core Functionality
- **Text-to-Image Generation**: Convert natural language prompts into high-quality images
- **Customizable Parameters**: Control inference steps, guidance scale, image dimensions, and random seed
- **Real-time Generation**: Watch your images come to life with animated loading states
- **One-Click Download**: Save generated images instantly

### 🎨 User Interface
- **Modern Dark Theme**: Beautiful gradient backgrounds and smooth animations
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Interactive Controls**: Advanced options panel with real-time slider updates
- **Example Prompts**: Pre-built prompt library for quick inspiration
- **Status Notifications**: Clear success/error/warning messages
- **Keyboard Shortcuts**: Ctrl+Enter / Cmd+Enter to generate images

### 🛠️ Technical Features
- **Modular Architecture**: Clean separation of concerns (routes, pipeline, config)
- **Error Handling**: Comprehensive error handling with detailed logging
- **Health Check API**: Monitor application status
- **Docker Support**: GPU and CPU containerization options
- **CI/CD Ready**: GitHub Actions workflow included
- **Environment Configuration**: Easy setup with environment variables


### Main Interface
```
┌─────────────────────────────────────────┐
│  🎨 AI Image Generator                  │
│  Transform your words into visuals      │
├─────────────────────────────────────────┤
│  Prompt: [Your imagination here...]     │
│                                          │
│  ▼ Advanced Options                     │
│    Steps: 28  Guidance: 7.5            │
│    Width: 512px  Height: 512px         │
│                                          │
│  [✨ Generate Image] [🎲 Random Prompt]│
├─────────────────────────────────────────┤
│  Generated Image:                       │
│  [Beautiful AI-generated image]         │
│  [📥 Download]                          │
└─────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- NVIDIA GPU with CUDA support (optional, for faster generation)
- 8GB+ RAM (16GB+ recommended)
- 10GB+ free disk space

### Installation

#### 1. Clone the Repository
```bash
git clone https://github.com/ruhul-cse-duet/text-to-image-create-diffusion-flask.git
cd text-to-image-diffusion
```

#### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Run the Application
```bashpython run.py
```

#### 5. Open Browser
Navigate to: **http://localhost:5000**

### 🎉 That's it! You're ready to generate images!

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root (optional):

```env
# Device Configuration
DEVICE=cpu                    # Options: cpu, cuda, cuda:0
HF_TOKEN=your_token_here     # Hugging Face token (if using gated models)

# Model Configuration
MODEL_ID=runwayml/stable-diffusion-v1-5

# Generation Parameters
NUM_INFERENCE_STEPS=28       # Range: 10-100 (higher = better quality, slower)
GUIDANCE_SCALE=7.5           # Range: 1-20 (higher = follows prompt more closely)
HEIGHT=512                   # Options: 256, 384, 512, 768, 1024 (must be divisible by 8)
WIDTH=512                    # Options: 256, 384, 512, 768, 1024 (must be divisible by 8)

# Application Settings
MAX_PROMPT_LENGTH=500
REQUEST_TIMEOUT=120
LOG_LEVEL=INFO
```

### GPU Acceleration (Recommended)

For **MUCH FASTER** generation (10-30 seconds vs 5-15 minutes):

#### Install CUDA-enabled PyTorch:
```bash
# For CUDA 11.8
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# For CUDA 12.1
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
```

#### Set Device to GPU:
```bash
# Windows
set DEVICE=cuda

# Linux/Mac
export DEVICE=cuda
```

#### Verify GPU:
```python
import torch
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"GPU: {torch.cuda.get_device_name(0)}")
```

## 📚 Usage Guide

### Basic Usage

1. **Enter a Prompt**: Describe the image you want to create
   ```
   Example: "A serene mountain landscape at sunset, photorealistic, 8k quality"
   ```

2. **Click Generate**: Wait for the AI to create your image
   - CPU: 5-15 minutes ⏳
   - GPU: 10-30 seconds ⚡

3. **Download**: Save your masterpiece!

### Advanced Options

Click "Advanced Options" to customize:

- **Inference Steps** (10-50): More steps = better quality but slower
- **Guidance Scale** (1-20): How closely the AI follows your prompt
- **Width & Height** (256-1024): Image dimensions (must be divisible by 8)
- **Seed** (optional): For reproducible results

### Example Prompts

**Photography Style:**
```
A professional portrait of an astronaut in space, Earth in background, 
dramatic lighting, National Geographic style, 8k, highly detailed
```

**Fantasy Art:**
```
A magical forest with bioluminescent mushrooms, fairy lights, 
moonlight filtering through ancient trees, fantasy art, ethereal
```

**Cyberpunk:**
```
Futuristic cyberpunk city at night, neon signs, rain-soaked streets, 
flying cars, blade runner aesthetic, cinematic, ultra detailed
```

**Nature:**
```
Majestic lion on a cliff at golden hour, cinematic lighting,
wildlife photography, highly detailed, 8k resolution
```

### Keyboard Shortcuts

- **Ctrl + Enter** / **Cmd + Enter**: Generate image
- **Click Example Cards**: Auto-fill prompt with pre-made examples

## 🐳 Docker Deployment

### CPU Version
```bash
# Build
docker build -t ai-image-generator .

# Run
docker run -p 5000:5000 ai-image-generator
```

### GPU Version (Requires NVIDIA Docker)
```bash
# Build
docker build -t ai-image-generator-gpu .

# Run with GPU
docker run --gpus all -p 5000:5000 -e DEVICE=cuda ai-image-generator-gpu
```

### Docker Compose
```bash
# CPU
docker-compose up --build

# GPU (edit docker-compose.yml to uncomment GPU runtime)
docker-compose up --build
```

## 🏗️ Project Structure

```
text-to-image-diffusion/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── config.py            # Configuration management
│   ├── pipeline.py          # Stable Diffusion pipeline
│   ├── routes.py            # API endpoints
│   ├── utils.py             # Helper functions
│   └── templates/
│       └── index.html       # Main UI template
├── static/
│   ├── script.js            # Frontend JavaScript
│   └── style.css            # Styling and animations
├── .github/
│   └── workflows/
│       └── ci.yml           # GitHub Actions CI/CD
├── Dockerfile               # Container configuration
├── docker-compose.yml       # Multi-container setup
├── requirements.txt         # Python dependencies
├── run.py                   # Application entry point
└── README.md               # This file
```

## 🔌 API Documentation

### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "pipeline_loaded": true,
  "device_info": {
    "device": "cuda:0",
    "device_type": "cuda",
    "gpu_name": "NVIDIA GeForce RTX 3080"
  }
}
```

### Generate Image
```http
POST /generate
Content-Type: application/json

{
  "prompt": "A beautiful sunset over mountains",
  "num_inference_steps": 28,
  "guidance_scale": 7.5,
  "width": 512,
  "height": 512,
  "seed": 42
}
```

**Response:**
```json
{
  "success": true,
  "image": "data:image/png;base64,iVBORw0KGgo...",
  "prompt": "A beautiful sunset over mountains",
  "parameters": {
    "steps": 28,
    "guidance": 7.5,
    "height": 512,
    "width": 512,
    "seed": 42
  }
}
```

## 🛠️ Development

### Running Tests
```bash
# Install dev dependencies
pip install pytest pytest-cov

# Run tests
pytest

# With coverage
pytest --cov=app tests/
```

### Code Quality
```bash
# Format code
black app/

# Lint
flake8 app/

# Type checking
mypy app/
```

### Hot Reload (Development)
```bash
# Enable Flask debug mode
export FLASK_DEBUG=1  # Linux/Mac
set FLASK_DEBUG=1     # Windows

python run.py
```

## 📊 Performance Benchmarks

| Hardware | Resolution | Steps | Time per Image |
|----------|------------|-------|----------------|
| CPU (Intel i7) | 512x512 | 28 | ~10-15 min ⏳ |
| RTX 3060 | 512x512 | 28 | ~15 sec ⚡ |
| RTX 3080 | 512x512 | 28 | ~10 sec ⚡ |
| RTX 4090 | 512x512 | 28 | ~5 sec ⚡ |
| RTX 4090 | 1024x1024 | 50 | ~20 sec ⚡ |

## 🐛 Troubleshooting

### Common Issues

#### 1. "Pipeline not loaded" Error
**Solution:** Wait for model to download (first run only). Check logs:
```bash
tail -f logs/app.log
```

#### 2. Out of Memory Error
**Solutions:**
- Reduce image size (try 384x384 or 256x256)
- Reduce inference steps (try 20 instead of 28)
- Close other applications
- Use CPU instead of GPU (slower but more memory efficient)

#### 3. Slow Generation on CPU
**This is normal!** CPU generation takes 5-15 minutes. Solutions:
- Use GPU (see GPU Acceleration section)
- Reduce steps to 15-20
- Reduce image size to 256x256

#### 4. Static Files Not Loading (404)
**Solution:** Already fixed in latest version. If issue persists:
```bash
# Verify static folder structure
ls -la static/
# Should contain: script.js and style.css
```

#### 5. "Accelerate" Import Error
**Solution:**
```bash
pip install --upgrade accelerate
```

### Getting Help

- **Issues**: Open an issue on GitHub
- **Questions**: Check existing issues or start a discussion
- **Email**: ruhul.cse.duet@gmail.com

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Stable Diffusion**: RunwayML and Stability AI
- **Diffusers Library**: Hugging Face Team
- **Flask**: Pallets Projects
- **Icons**: Heroicons
- **Fonts**: Google Fonts (Inter)

## 🌟 Star History

If you find this project useful, please consider giving it a star ⭐

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📮 Contact

**Project Maintainer**: Ruhul Amin
- GitHub: [@ruhul-cse-duet](https://github.com/yourusername)
- Email: ruhul.cse.duet@gmail.com
- LinkedIn: [@ruhul-duet-cse/](https://linkedin.com/in/yourprofile)

## 🔮 Roadmap

- [ ] Multiple model support (SD 2.1, SDXL)
- [ ] Image-to-image generation
- [ ] Inpainting support
- [ ] Batch generation
- [ ] User authentication
- [ ] Gallery/history feature
- [ ] Prompt templates library
- [ ] API rate limiting
- [ ] Redis caching
- [ ] S3 storage integration

---

<div align="center">

**Made with ❤️ and 🤖 AI**

[⬆ Back to Top](#-ai-image-generator---text-to-image-with-stable-diffusion)

</div>
