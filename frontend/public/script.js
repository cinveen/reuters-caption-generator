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
const addInfoButton = document.getElementById('addInfoButton');
const startOverButton = document.getElementById('startOverButton');
const missingInfoAlert = document.getElementById('missingInfoAlert');
const missingInfoList = document.getElementById('missingInfoList');
const recordAdditionalButton = document.getElementById('recordAdditionalButton');
const stopAdditionalButton = document.getElementById('stopAdditionalButton');
const additionalRecordingStatus = document.getElementById('additionalRecordingStatus');
const additionalAudioPlayback = document.getElementById('additionalAudioPlayback');
const additionalDetails = document.getElementById('additionalDetails');
const updateButton = document.getElementById('updateButton');
const cancelAddButton = document.getElementById('cancelAddButton');
const missingInfoReminder = document.getElementById('missingInfoReminder');
const loadingOverlay = document.getElementById('loadingOverlay');
const loadingMessage = document.getElementById('loadingMessage');
const toast = document.getElementById('toast');
const toastMessage = document.getElementById('toastMessage');

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
    updateButton.addEventListener('click', updateCaption);
    cancelAddButton.addEventListener('click', () => showStep('stepResult'));

    // Enable typing in additional details
    additionalDetails.addEventListener('input', () => {
        if (additionalDetails.value.trim()) {
            updateButton.disabled = false;
        }
    });

    // Check browser support
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        showToast('⚠️ Audio recording not supported in this browser');
        recordButton.disabled = true;
    }
}

// Step Navigation
function showStep(stepId) {
    const steps = [stepRecord, stepGenerate, stepResult, stepAddDetails];
    steps.forEach(step => step.classList.remove('active'));
    document.getElementById(stepId).classList.add('active');
}

// Recording Functions
async function startRecording() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        audioChunks = [];

        mediaRecorder.ondataavailable = (e) => {
            if (e.data.size > 0) audioChunks.push(e.data);
        };

        mediaRecorder.onstop = processRecording;
        mediaRecorder.start();

        recordButton.classList.add('hidden');
        stopButton.classList.remove('hidden');
        recordingStatus.textContent = 'Recording...';
        recordingStatus.classList.add('recording');
        audioPlayback.classList.add('hidden');

    } catch (error) {
        showToast(`⚠️ ${error.message}`);
    }
}

function stopRecording() {
    if (mediaRecorder && mediaRecorder.state !== 'inactive') {
        mediaRecorder.stop();
        mediaRecorder.stream.getTracks().forEach(track => track.stop());

        stopButton.classList.add('hidden');
        recordingStatus.textContent = 'Processing...';
        recordingStatus.classList.remove('recording');

        showLoading('Transcribing...');
    }
}

function processRecording() {
    const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
    audioPlayback.src = URL.createObjectURL(audioBlob);
    audioPlayback.classList.remove('hidden');

    uploadAudio(audioBlob);
}

async function uploadAudio(blob) {
    try {
        const formData = new FormData();
        formData.append('audio_blob', blob);

        const response = await fetch(API_UPLOAD_AUDIO, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) throw new Error(`Server error: ${response.status}`);

        const data = await response.json();
        currentTranscription = data.transcription;
        transcriptionPreview.textContent = `"${truncate(currentTranscription, 150)}..."`;

        hideLoading();
        showStep('stepGenerate');
        recordButton.classList.remove('hidden');
        recordingStatus.textContent = '';

    } catch (error) {
        hideLoading();
        showToast(`⚠️ Error: ${error.message}`);
        recordButton.classList.remove('hidden');
        recordingStatus.textContent = '';
    }
}

// Caption Generation
async function generateCaption() {
    try {
        showLoading('Generating caption...');

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
    formattedCaption.value = data.formatted_caption || 'Could not generate caption.';

    // Handle missing information
    if (data.missing_information && data.missing_information.length > 0) {
        storedMissingInfo = data.missing_information;
        missingInfoList.innerHTML = '';
        data.missing_information.forEach(item => {
            const li = document.createElement('li');
            li.textContent = item;
            missingInfoList.appendChild(li);
        });
        missingInfoAlert.classList.remove('hidden');
        addInfoButton.classList.remove('hidden');
    } else {
        missingInfoAlert.classList.add('hidden');
        addInfoButton.classList.add('hidden');
    }
}

// Additional Details Recording
async function startAdditionalRecording() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        additionalMediaRecorder = new MediaRecorder(stream);
        additionalAudioChunks = [];

        additionalMediaRecorder.ondataavailable = (e) => {
            if (e.data.size > 0) additionalAudioChunks.push(e.data);
        };

        additionalMediaRecorder.onstop = processAdditionalRecording;
        additionalMediaRecorder.start();

        recordAdditionalButton.classList.add('hidden');
        stopAdditionalButton.classList.remove('hidden');
        additionalRecordingStatus.textContent = 'Recording...';
        additionalRecordingStatus.classList.add('recording');

    } catch (error) {
        showToast(`⚠️ ${error.message}`);
    }
}

function stopAdditionalRecording() {
    if (additionalMediaRecorder && additionalMediaRecorder.state !== 'inactive') {
        additionalMediaRecorder.stop();
        additionalMediaRecorder.stream.getTracks().forEach(track => track.stop());

        stopAdditionalButton.classList.add('hidden');
        additionalRecordingStatus.textContent = 'Processing...';
        additionalRecordingStatus.classList.remove('recording');

        showLoading('Transcribing...');
    }
}

function processAdditionalRecording() {
    const audioBlob = new Blob(additionalAudioChunks, { type: 'audio/wav' });
    additionalAudioPlayback.src = URL.createObjectURL(audioBlob);
    additionalAudioPlayback.classList.remove('hidden');

    uploadAdditionalAudio(audioBlob);
}

async function uploadAdditionalAudio(blob) {
    try {
        const formData = new FormData();
        formData.append('audio_blob', blob);

        const response = await fetch(API_UPLOAD_AUDIO, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) throw new Error(`Server error: ${response.status}`);

        const data = await response.json();

        const existing = additionalDetails.value.trim();
        additionalDetails.value = existing
            ? `${existing}\n\n${data.transcription}`
            : data.transcription;

        updateButton.disabled = false;
        recordAdditionalButton.classList.remove('hidden');
        additionalRecordingStatus.textContent = '';
        hideLoading();

    } catch (error) {
        hideLoading();
        showToast(`⚠️ Error: ${error.message}`);
        recordAdditionalButton.classList.remove('hidden');
        additionalRecordingStatus.textContent = '';
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

// Show missing info when entering add details step
addInfoButton.addEventListener('click', () => {
    if (storedMissingInfo.length > 0) {
        missingInfoReminder.innerHTML = '<strong>Missing:</strong><ul>' +
            storedMissingInfo.map(item => `<li>${item}</li>`).join('') +
            '</ul>';
    }

    // Clear the textarea and audio for fresh input
    additionalDetails.value = '';
    additionalAudioPlayback.src = '';
    additionalAudioPlayback.classList.add('hidden');
    updateButton.disabled = true;

    showStep('stepAddDetails');
});
