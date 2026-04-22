/**
 * CalcuBite - Frontend Application
 * Handles image upload, preview, and API communication
 */

// DOM Elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const previewImage = document.getElementById('previewImage');
const removeBtn = document.getElementById('removeImage');
const analyzeBtn = document.getElementById('analyzeBtn');
const uploadSection = document.getElementById('uploadSection');
const loadingSection = document.getElementById('loadingSection');
const resultsSection = document.getElementById('resultsSection');
const errorSection = document.getElementById('errorSection');
const newAnalysisBtn = document.getElementById('newAnalysisBtn');
const retryBtn = document.getElementById('retryBtn');

// Loading steps
const steps = [
    document.getElementById('step1'),
    document.getElementById('step2'),
    document.getElementById('step3')
];

let currentFile = null;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
});

function setupEventListeners() {
    // Upload area click
    uploadArea.addEventListener('click', (e) => {
        if (e.target !== removeBtn && !removeBtn.contains(e.target)) {
            fileInput.click();
        }
    });

    // File input change
    fileInput.addEventListener('change', handleFileSelect);

    // Drag and drop
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleDrop);

    // Remove image
    removeBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        removeImage();
    });

    // Analyze button
    analyzeBtn.addEventListener('click', analyzeImage);

    // New analysis button
    newAnalysisBtn.addEventListener('click', resetApp);

    // Retry button
    retryBtn.addEventListener('click', () => {
        hideSection(errorSection);
        showSection(uploadSection);
    });
}

function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        processFile(file);
    }
}

function handleDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    uploadArea.classList.add('dragover');
}

function handleDragLeave(e) {
    e.preventDefault();
    e.stopPropagation();
    uploadArea.classList.remove('dragover');
}

function handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    uploadArea.classList.remove('dragover');

    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
        processFile(file);
    } else {
        showError('Please drop an image file (JPG, PNG, GIF, WebP)');
    }
}

function processFile(file) {
    // Validate file type
    const allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];
    if (!allowedTypes.includes(file.type)) {
        showError('Invalid file type. Please use JPG, PNG, GIF, or WebP.');
        return;
    }

    // Validate file size (16MB)
    const maxSize = 16 * 1024 * 1024;
    if (file.size > maxSize) {
        showError('File too large. Maximum size is 16MB.');
        return;
    }

    currentFile = file;

    // Show preview
    const reader = new FileReader();
    reader.onload = (e) => {
        previewImage.src = e.target.result;
        previewImage.classList.remove('hidden');
        removeBtn.classList.remove('hidden');
        uploadArea.querySelector('.upload-placeholder').classList.add('hidden');
        analyzeBtn.disabled = false;
    };
    reader.readAsDataURL(file);
}

function removeImage() {
    currentFile = null;
    fileInput.value = '';
    previewImage.src = '';
    previewImage.classList.add('hidden');
    removeBtn.classList.add('hidden');
    uploadArea.querySelector('.upload-placeholder').classList.remove('hidden');
    analyzeBtn.disabled = true;
}

async function analyzeImage() {
    if (!currentFile) return;

    // Show loading
    hideSection(uploadSection);
    showSection(loadingSection);

    // Animate loading steps
    animateLoadingSteps();

    // Prepare form data
    const formData = new FormData();
    formData.append('image', currentFile);

    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (response.ok && data.success) {
            displayResults(data);
        } else {
            showError(data.error || 'Analysis failed. Please try again.');
        }
    } catch (error) {
        console.error('Error:', error);
        showError('Network error. Please check your connection and try again.');
    }
}

function animateLoadingSteps() {
    // Reset steps
    steps.forEach(step => {
        step.classList.remove('active', 'completed');
    });

    // Animate through steps
    let currentStep = 0;
    
    function activateStep() {
        if (currentStep > 0) {
            steps[currentStep - 1].classList.remove('active');
            steps[currentStep - 1].classList.add('completed');
        }
        
        if (currentStep < steps.length) {
            steps[currentStep].classList.add('active');
            currentStep++;
            setTimeout(activateStep, 2000);
        }
    }

    activateStep();
}

function displayResults(data) {
    hideSection(loadingSection);
    showSection(resultsSection);

    // Set result image
    document.getElementById('resultImage').src = previewImage.src;

    // Set food info
    document.getElementById('foodName').textContent = data.food_name || 'Unknown Food';
    
    // Set confidence badge
    const confidenceBadge = document.getElementById('confidenceBadge');
    const confidence = data.confidence || 'Unknown';
    confidenceBadge.textContent = confidence;
    confidenceBadge.className = 'confidence-badge';
    if (confidence.toLowerCase().includes('medium')) {
        confidenceBadge.classList.add('medium');
    } else if (confidence.toLowerCase().includes('low')) {
        confidenceBadge.classList.add('low');
    }

    // Set portion estimate
    document.getElementById('portionEstimate').textContent = 
        data.portion_estimate ? `Estimated portion: ${data.portion_estimate}` : 'Portion estimate unavailable';

    // Set nutrition values
    const nutrition = data.nutrition || {};
    document.getElementById('calories').textContent = formatNumber(nutrition.calories);
    document.getElementById('protein').textContent = formatNumber(nutrition.protein);
    document.getElementById('carbs').textContent = formatNumber(nutrition.carbs);
    document.getElementById('fat').textContent = formatNumber(nutrition.fat);
    document.getElementById('fiber').textContent = formatNumber(nutrition.fiber);
    document.getElementById('sugar').textContent = formatNumber(nutrition.sugar);

    // Set health insights
    document.getElementById('healthInsights').textContent = 
        data.health_insights || 'No health insights available.';

    // Set dietary tags
    const tagsContainer = document.getElementById('dietaryTags');
    tagsContainer.innerHTML = '';
    
    if (data.dietary_category) {
        const categories = data.dietary_category.split(',').map(c => c.trim()).filter(c => c);
        categories.forEach(category => {
            const tag = document.createElement('span');
            tag.className = 'dietary-tag';
            tag.textContent = category;
            tagsContainer.appendChild(tag);
        });
    }

    // Set raw analysis (for debugging)
    if (data.raw_analysis) {
        document.getElementById('rawText').textContent = data.raw_analysis;
    }
}

function formatNumber(value) {
    if (value === null || value === undefined || isNaN(value)) return '0';
    return Math.round(value).toString();
}

function showError(message) {
    hideSection(loadingSection);
    hideSection(uploadSection);
    hideSection(resultsSection);
    showSection(errorSection);
    document.getElementById('errorMessage').textContent = message;
}

function resetApp() {
    removeImage();
    hideSection(resultsSection);
    showSection(uploadSection);
}

function showSection(section) {
    section.classList.remove('hidden');
}

function hideSection(section) {
    section.classList.add('hidden');
}

// Prevent default drag behaviors on document
document.addEventListener('dragover', (e) => e.preventDefault());
document.addEventListener('drop', (e) => e.preventDefault());
