// ========================================
// State Management
// ========================================

const state = {
    isGenerating: false,
    lastGeneratedImage: null
};

// ========================================
// DOM Elements
// ========================================

const elements = {
    promptTextarea: document.getElementById('prompt'),
    charCount: document.getElementById('charCount'),
    generateBtn: document.getElementById('generateBtn'),
    randomBtn: document.getElementById('randomBtn'),
    advancedToggle: document.getElementById('advancedToggle'),
    advancedContent: document.getElementById('advancedContent'),
    
    // Sliders
    stepsSlider: document.getElementById('steps'),
    stepsValue: document.getElementById('stepsValue'),
    guidanceSlider: document.getElementById('guidance'),
    guidanceValue: document.getElementById('guidanceValue'),
    widthSlider: document.getElementById('width'),
    widthValue: document.getElementById('widthValue'),
    heightSlider: document.getElementById('height'),
    heightValue: document.getElementById('heightValue'),    seedInput: document.getElementById('seed'),
    
    // Output
    outputSection: document.getElementById('outputSection'),
    loader: document.getElementById('loader'),
    generatedImage: document.getElementById('generatedImage'),
    imageDetails: document.getElementById('imageDetails'),
    downloadBtn: document.getElementById('downloadBtn'),
    
    // Details
    detailPrompt: document.getElementById('detailPrompt'),
    detailSteps: document.getElementById('detailSteps'),
    detailGuidance: document.getElementById('detailGuidance'),
    detailDimensions: document.getElementById('detailDimensions'),
    
    // Status
    status: document.getElementById('status'),
    statusMessage: document.getElementById('statusMessage')
};

// ========================================
// Random Prompts
// ========================================

const randomPrompts = [
    "A majestic mountain landscape at golden hour, snow-capped peaks, alpine meadow with wildflowers, cinematic lighting, highly detailed, 8k",
    "Futuristic cyberpunk street market at night, neon signs in Japanese and English, rain-soaked pavement, flying vehicles, blade runner aesthetic",
    "Ancient library with towering bookshelves, magical glowing books, spiral staircase, warm candlelight, fantasy art style",
    "Underwater coral reef scene, tropical fish, sea turtle, rays of sunlight penetrating water, National Geographic quality",
    "Cozy coffee shop interior, vintage furniture, plants, large windows with rain outside, warm ambient lighting, photorealistic",
    "Portrait of a wise elderly wizard, long white beard, pointed hat, magical staff, mystical aura, detailed facial features, fantasy character design",
    "Minimalist modern architecture, white concrete building, geometric shapes, blue sky, architectural photography style",
    "Vibrant street food market in Southeast Asia, colorful stalls, steam rising from food, bustling crowd, documentary photography",
    "Peaceful zen garden, raked sand patterns, stone lanterns, bamboo fountain, maple trees, Japanese aesthetic",
    "Space station interior, astronauts floating, Earth visible through large windows, high-tech equipment, sci-fi realistic"
];

// ========================================
// Utility Functions
// ========================================

function showStatus(message, type = 'info') {
    elements.status.className = `status-card ${type}`;
    elements.statusMessage.textContent = message;
    elements.status.classList.remove('hidden');
    
    // Auto-hide after 5 seconds for success/info
    if (type === 'success' || type === 'info') {
        setTimeout(() => {
            elements.status.classList.add('hidden');
        }, 5000);
    }
}

function hideStatus() {
    elements.status.classList.add('hidden');
}

function setGeneratingState(isGenerating) {
    state.isGenerating = isGenerating;
    elements.generateBtn.disabled = isGenerating;
    
    if (isGenerating) {
        elements.generateBtn.innerHTML = `
            <svg class="btn-icon spinner" width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                <circle cx="10" cy="10" r="8" stroke="currentColor" stroke-width="2" fill="none" opacity="0.3"/>
                <path d="M10 2 A 8 8 0 0 1 18 10" stroke="currentColor" stroke-width="2" fill="none"/>
            </svg>
            <span>Generating...</span>
        `;
    } else {
        elements.generateBtn.innerHTML = `
            <svg class="btn-icon" width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                <path d="M10 2L13 8L19 9L14.5 13L16 19L10 16L4 19L5.5 13L1 9L7 8L10 2Z"/>
            </svg>
            <span>Generate Image</span>
        `;
    }
}

function updateCharCount() {
    const count = elements.promptTextarea.value.length;
    elements.charCount.textContent = count;
    
    if (count > 450) {
        elements.charCount.style.color = 'var(--warning)';
    } else {
        elements.charCount.style.color = 'var(--text-muted)';
    }
}

function updateSliderValue(sliderId, valueId) {
    const slider = document.getElementById(sliderId);
    const valueDisplay = document.getElementById(valueId);
    valueDisplay.textContent = slider.value;
}

// ========================================
// API Functions
// ========================================

async function generateImage() {
    const prompt = elements.promptTextarea.value.trim();
    
    // Validate prompt
    if (!prompt) {
        showStatus('Please enter a prompt', 'warning');
        return;
    }
    
    if (state.isGenerating) {
        return;
    }
    
    // Collect parameters
    const params = {
        prompt: prompt,
        num_inference_steps: parseInt(elements.stepsSlider.value),
        guidance_scale: parseFloat(elements.guidanceSlider.value),
        width: parseInt(elements.widthSlider.value),
        height: parseInt(elements.heightSlider.value)
    };
    
    // Add seed if provided
    const seedValue = elements.seedInput.value.trim();
    if (seedValue) {
        params.seed = parseInt(seedValue);
    }
    
    try {
        setGeneratingState(true);
        hideStatus();
        
        // Show output section and loader
        elements.outputSection.classList.remove('hidden');
        elements.loader.classList.remove('hidden');
        elements.generatedImage.classList.add('hidden');
        elements.imageDetails.classList.add('hidden');
        
        // Make API call
        const response = await fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(params)
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            // Display image
            elements.generatedImage.src = data.image;
            elements.generatedImage.classList.remove('hidden');
            elements.loader.classList.add('hidden');
            
            // Update details
            elements.detailPrompt.textContent = data.prompt;
            elements.detailSteps.textContent = data.parameters.steps;
            elements.detailGuidance.textContent = data.parameters.guidance;
            elements.detailDimensions.textContent = `${data.parameters.width}x${data.parameters.height}`;
            elements.imageDetails.classList.remove('hidden');
            
            // Store for download
            state.lastGeneratedImage = data.image;
            
            showStatus('Image generated successfully!', 'success');
        } else {
            // Handle error
            const errorMsg = data.error || 'Failed to generate image';
            showStatus(errorMsg, 'error');
            elements.loader.classList.add('hidden');
        }
        
    } catch (error) {
        console.error('Generation error:', error);
        showStatus('Network error: Could not connect to server', 'error');
        elements.loader.classList.add('hidden');
    } finally {
        setGeneratingState(false);
    }
}

function setRandomPrompt() {
    const randomIndex = Math.floor(Math.random() * randomPrompts.length);
    elements.promptTextarea.value = randomPrompts[randomIndex];
    updateCharCount();
}

function downloadImage() {
    if (!state.lastGeneratedImage) {
        showStatus('No image to download', 'warning');
        return;
    }
    
    try {
        const link = document.createElement('a');
        link.href = state.lastGeneratedImage;
        link.download = `generated-image-${Date.now()}.png`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        showStatus('Image downloaded!', 'success');
    } catch (error) {
        console.error('Download error:', error);
        showStatus('Failed to download image', 'error');
    }
}

// ========================================
// Event Listeners
// ========================================

function initializeEventListeners() {
    // Character count
    elements.promptTextarea.addEventListener('input', updateCharCount);
    
    // Generate button
    elements.generateBtn.addEventListener('click', generateImage);
    
    // Random prompt button
    elements.randomBtn.addEventListener('click', setRandomPrompt);
    
    // Download button
    elements.downloadBtn.addEventListener('click', downloadImage);
    
    // Advanced toggle
    elements.advancedToggle.addEventListener('click', () => {
        elements.advancedToggle.classList.toggle('active');
        elements.advancedContent.classList.toggle('visible');
    });
    
    // Slider updates
    elements.stepsSlider.addEventListener('input', () => {
        updateSliderValue('steps', 'stepsValue');
    });
    
    elements.guidanceSlider.addEventListener('input', () => {
        updateSliderValue('guidance', 'guidanceValue');
    });
    
    elements.widthSlider.addEventListener('input', () => {
        updateSliderValue('width', 'widthValue');
    });
    
    elements.heightSlider.addEventListener('input', () => {
        updateSliderValue('height', 'heightValue');
    });
    
    // Example cards
    document.querySelectorAll('.example-card').forEach(card => {
        card.addEventListener('click', () => {
            const prompt = card.getAttribute('data-prompt');
            elements.promptTextarea.value = prompt;
            updateCharCount();
            
            // Scroll to prompt
            elements.promptTextarea.scrollIntoView({ behavior: 'smooth', block: 'center' });
            
            // Visual feedback
            card.style.transform = 'scale(0.95)';
            setTimeout(() => {
                card.style.transform = '';
            }, 200);
        });
    });
    
    // Enter key to generate (Ctrl+Enter or Cmd+Enter)
    elements.promptTextarea.addEventListener('keydown', (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            generateImage();
        }
    });
}

// ========================================
// Initialization
// ========================================

document.addEventListener('DOMContentLoaded', () => {
    console.log('Initializing AI Image Generator...');
    
    // Initialize event listeners
    initializeEventListeners();
    
    // Set initial values
    updateCharCount();
    
    // Check server health
    fetch('/health')
        .then(response => response.json())
        .then(data => {
            if (data.status === 'healthy') {
                console.log('Server is healthy:', data);
                showStatus('Ready to generate images!', 'success');
            } else {
                console.warn('Server not ready:', data);
                showStatus('Server is loading model... Please wait', 'warning');
            }
        })
        .catch(error => {
            console.error('Health check failed:', error);
            showStatus('Cannot connect to server', 'error');
        });
    
    console.log('Initialization complete!');
});
