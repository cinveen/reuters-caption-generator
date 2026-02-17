/**
 * Reuters Photo Caption Generator - Simplified Wizard UI
 * Step-by-step interface for tech-averse photographers
 */

// DOM Elements
const recordButton = document.getElementById('recordButton');
const stopButton = document.getElementById('stopButton');
const recordingStatus = document.getElementById('recordingStatus');
const audioPlayback = document.getElementById('audioPlayback');
const generateButton = document.getElementById('generateButton');
const transcriptionPreview = document.getElementById('transcriptionPreview');
const formattedCaption = document.getElementById('formattedCaption');
const copyButton = document.getElementById('copyButton');
const startOverButton = document.getElementById('startOverButton');
const showTypeButton = document.getElementById('showTypeButton');
const missingInfoAlert = document.getElementById('missingInfoAlert');
const missingInfoList = document.getElementById('missingInfoList');
const recordAdditionalButton = document.getElementById('recordAdditionalButton');
const stopAdditionalButton = document.getElementById('stopAdditionalButton');
const additionalRecordingStatus = document.getElementById('additionalRecordingStatus');
const additionalDetails = document.getElementById('additionalDetails');
const updateButton = document.getElementById('updateButton');
const loadingOverlay = document.getElementById('loadingOverlay');
const loadingMessage = document.getElementById('loadingMessage');
const toast = document.getElementById('toast');
const toastMessage = document.getElementById('toastMessage');

// Random background image
const backgroundImages = [
    'images/backgrounds/rugby.jpg',
    'images/backgrounds/arctic.jpg',
    'images/backgrounds/carnival.jpg',
    'images/backgrounds/lunar-indonesia.jpg',
    'images/backgrounds/lunar-russia.jpg',
    'images/backgrounds/lunar-thailand.jpg',
    'images/backgrounds/olympics-skijumping.jpg',
    'images/backgrounds/olympics-snowboard.jpg',
    'images/backgrounds/gaza.jpg'
];

// Set random background on page load
function setRandomBackground() {
    const randomImage = backgroundImages[Math.floor(Math.random() * backgroundImages.length)];
    document.body.style.backgroundImage = `url('${randomImage}')`;
}

// Initialize background
setRandomBackground();

// Step sections
const stepRecord = document.getElementById('stepRecord');
const stepGenerate = document.getElementById('stepGenerate');
const stepResult = document.getElementById('stepResult');
const stepAddDetails = document.getElementById('stepAddDetails');

// API Endpoints
const API_UPLOAD_AUDIO = '/api/upload-audio';
const API_GENERATE_CAPTION = '/api/generate-caption';

// Global state
let mediaRecorder;
let audioChunks = [];
let currentTranscription = '';
let additionalMediaRecorder;
let additionalAudioChunks = [];
let storedMissingInfo = [];

// Initialize
document.addEventListener('DOMContentLoaded', init);

function init() {
    // Button event listeners
    recordButton.addEventListener('click', startRecording);
    stopButton.addEventListener('click', stopRecording);
    generateButton.addEventListener('click', generateCaption);
    copyButton.addEventListener('click', copyToClipboard);
    startOverButton.addEventListener('click', startOver);
    recordAdditionalButton.addEventListener('click', startAdditionalRecording);
    stopAdditionalButton.addEventListener('click', stopAdditionalRecording);
    showTypeButton.addEventListener('click', toggleTypeSection);
    updateButton.addEventListener('click', updateCaption);

    // Enable typing in additional details
    additionalDetails.addEventListener('input', () => {
        if (additionalDetails.value.trim()) {
            updateButton.disabled = false;
        }
    });

    // Note: We're now using native Python audio recording via pywebview.api
    // No browser MediaRecorder needed!
    console.log('Reuters Caption Generator initialized with native audio recording');
}

// Step Navigation
function showStep(stepId) {
    const steps = [stepRecord, stepGenerate, stepResult, stepAddDetails];
    steps.forEach(step => step.classList.remove('active'));
    document.getElementById(stepId).classList.add('active');
}

// Recording Functions - Using Native Python API
async function startRecording() {
    try {
        console.log('Starting native recording via Python...');

        // Call Python function via pywebview API bridge
        const result = await pywebview.api.start_recording();

        if (!result.success) {
            throw new Error(result.error || 'Failed to start recording');
        }

        recordButton.classList.add('hidden');
        stopButton.classList.remove('hidden');
        recordingStatus.textContent = 'Recording...';
        recordingStatus.classList.add('recording');
        audioPlayback.classList.add('hidden');

    } catch (error) {
        showToast(`⚠️ ${error.message}`);
        console.error('Recording error:', error);
    }
}

async function stopRecording() {
    try {
        stopButton.classList.add('hidden');
        recordingStatus.textContent = 'Processing...';
        recordingStatus.classList.remove('recording');
        showLoading('Transcribing...');

        console.log('Stopping recording and transcribing...');

        // Call Python function - it records, stops, and transcribes all in one!
        const result = await pywebview.api.stop_recording();

        if (!result.success) {
            throw new Error(result.error || 'Failed to process recording');
        }

        // Set the transcription
        currentTranscription = result.transcription;

        // Auto-generate caption immediately (skip preview step)
        recordButton.classList.remove('hidden');
        recordingStatus.textContent = '';

        // Automatically generate caption
        await generateCaption();

    } catch (error) {
        hideLoading();
        showToast(`⚠️ Error: ${error.message}`);
        recordButton.classList.remove('hidden');
        recordingStatus.textContent = '';
        console.error('Stop recording error:', error);
    }
}

// Caption Generation
async function generateCaption() {
    try {
        // Show different message if updating vs. initial generation
        const isUpdate = formattedCaption.value.trim().length > 0;
        showLoading(isUpdate ? 'Updating caption...' : 'Generating caption...');

        const transcriptionToUse = additionalDetails.value.trim()
            ? `${currentTranscription}\n\nAdditional details: ${additionalDetails.value.trim()}`
            : currentTranscription;

        const response = await fetch(API_GENERATE_CAPTION, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ transcription: transcriptionToUse })
        });

        if (!response.ok) throw new Error(`Server error: ${response.status}`);

        const data = await response.json();
        displayCaption(data);
        hideLoading();
        showStep('stepResult');

    } catch (error) {
        hideLoading();
        showToast(`⚠️ Error: ${error.message}`);
    }
}

function displayCaption(data) {
    console.log('displayCaption received:', data);
    console.log('missing_information:', data.missing_information);
    console.log('missing_information length:', data.missing_information ? data.missing_information.length : 'undefined');

    formattedCaption.value = data.formatted_caption || 'Could not generate caption.';

    // Handle missing information
    const additionalDetailsSection = document.getElementById('additionalDetailsSection');
    if (data.missing_information && data.missing_information.length > 0) {
        storedMissingInfo = data.missing_information;
        missingInfoList.innerHTML = '';
        data.missing_information.forEach(item => {
            const li = document.createElement('li');
            li.textContent = item;
            missingInfoList.appendChild(li);
        });
        missingInfoAlert.classList.remove('hidden');
        additionalDetailsSection.classList.remove('hidden');
    } else {
        missingInfoAlert.classList.add('hidden');
        additionalDetailsSection.classList.add('hidden');
    }
}

// Additional Details Recording - Using Native Python API
async function startAdditionalRecording() {
    try {
        console.log('Starting additional recording via Python...');

        const result = await pywebview.api.start_recording();

        if (!result.success) {
            throw new Error(result.error || 'Failed to start recording');
        }

        recordAdditionalButton.classList.add('hidden');
        stopAdditionalButton.classList.remove('hidden');
        additionalRecordingStatus.textContent = 'Recording...';
        additionalRecordingStatus.classList.add('recording');

    } catch (error) {
        showToast(`⚠️ ${error.message}`);
        console.error('Additional recording error:', error);
    }
}

async function stopAdditionalRecording() {
    try {
        stopAdditionalButton.classList.add('hidden');
        additionalRecordingStatus.textContent = 'Processing...';
        additionalRecordingStatus.classList.remove('recording');
        showLoading('Transcribing...');

        console.log('Stopping additional recording and transcribing...');

        const result = await pywebview.api.stop_recording();

        if (!result.success) {
            throw new Error(result.error || 'Failed to process recording');
        }

        // Merge with current transcription
        currentTranscription = currentTranscription + '\n\nAdditional details: ' + result.transcription;

        // Reset UI
        recordAdditionalButton.classList.remove('hidden');
        additionalRecordingStatus.textContent = '';

        // Auto-generate updated caption
        await generateCaption();

    } catch (error) {
        hideLoading();
        showToast(`⚠️ Error: ${error.message}`);
        recordAdditionalButton.classList.remove('hidden');
        additionalRecordingStatus.textContent = '';
        console.error('Stop additional recording error:', error);
    }
}

// Toggle type section visibility
function toggleTypeSection() {
    const typeSection = document.getElementById('typeSection');
    typeSection.classList.toggle('hidden');

    if (!typeSection.classList.contains('hidden')) {
        additionalDetails.focus();
    }
}

function updateCaption() {
    if (!additionalDetails.value.trim()) {
        showToast('⚠️ Please add some details first');
        return;
    }

    // Merge additional details into the main transcription for next iteration
    currentTranscription = currentTranscription + '\n\nAdditional details: ' + additionalDetails.value.trim();
    additionalDetails.value = ''; // Clear for next round

    // Hide type section after updating
    const typeSection = document.getElementById('typeSection');
    typeSection.classList.add('hidden');

    generateCaption();
}

// UI Actions
function copyToClipboard() {
    formattedCaption.select();
    document.execCommand('copy');
    showToast('✓ Copied to clipboard!');
}

function startOver() {
    // Reset state
    currentTranscription = '';
    additionalDetails.value = '';
    formattedCaption.value = '';
    recordingStatus.textContent = '';
    additionalRecordingStatus.textContent = '';
    audioPlayback.src = '';
    additionalAudioPlayback.src = '';
    storedMissingInfo = [];

    // Reset buttons
    recordButton.classList.remove('hidden');
    stopButton.classList.add('hidden');
    recordAdditionalButton.classList.remove('hidden');
    stopAdditionalButton.classList.add('hidden');
    audioPlayback.classList.add('hidden');
    additionalAudioPlayback.classList.add('hidden');
    updateButton.disabled = true;

    // Go to first step
    showStep('stepRecord');
}

// Utility Functions
function showLoading(message) {
    loadingMessage.textContent = message;
    loadingOverlay.classList.add('active');
}

function hideLoading() {
    loadingOverlay.classList.remove('active');
}

function showToast(message) {
    toastMessage.textContent = message;
    toast.classList.add('show');
    setTimeout(() => toast.classList.remove('show'), 3000);
}

function truncate(str, maxLen) {
    return str.length > maxLen ? str.substring(0, maxLen) : str;
}

// Additional details section is now inline on result page
// No need for separate step navigation
