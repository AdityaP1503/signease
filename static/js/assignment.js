/**
 * SignEase - Daily Assignment Webcam & Real-time Gesture Recognition
 */

let videoElement = null;
let canvasElement = null;
let mediaStream = null;
let isCameraActive = false;
let isProcessing = false;

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', () => {
    videoElement = document.getElementById('webcam-video');
    canvasElement = document.getElementById('webcam-canvas');

    const startBtn = document.getElementById('btn-start-camera');
    const stopBtn = document.getElementById('btn-stop-camera');
    const checkBtn = document.getElementById('btn-check-sign');
    const retryBtn = document.getElementById('btn-retry-sign');

    if (startBtn) startBtn.addEventListener('click', startWebcam);
    if (stopBtn) stopBtn.addEventListener('click', stopWebcam);
    if (checkBtn) checkBtn.addEventListener('click', captureAndRecognize);
    if (retryBtn) retryBtn.addEventListener('click', resetFeedbackCard);

    // Auto cleanup camera when navigating away
    window.addEventListener('beforeunload', stopWebcam);
    window.addEventListener('pagehide', stopWebcam);
});

async function startWebcam() {
    if (isCameraActive) return;

    const placeholder = document.getElementById('camera-placeholder');
    const liveIndicator = document.getElementById('camera-live-indicator');
    const startBtn = document.getElementById('btn-start-camera');
    const stopBtn = document.getElementById('btn-stop-camera');
    const checkBtn = document.getElementById('btn-check-sign');

    try {
        const constraints = {
            video: {
                width: { ideal: 640 },
                height: { ideal: 480 },
                facingMode: 'user'
            },
            audio: false
        };

        mediaStream = await navigator.mediaDevices.getUserMedia(constraints);
        videoElement.srcObject = mediaStream;
        await videoElement.play();

        isCameraActive = true;
        if (placeholder) placeholder.classList.add('d-none');
        if (videoElement) videoElement.classList.remove('d-none');
        if (liveIndicator) liveIndicator.classList.remove('d-none');

        if (startBtn) startBtn.classList.add('d-none');
        if (stopBtn) stopBtn.classList.remove('d-none');
        if (checkBtn) checkBtn.disabled = false;

        updateFeedbackMessage('neutral', 'Camera active! Hold your hand in position and click "Check Sign" or "Submit Answer".', null);
    } catch (err) {
        console.error('Error starting camera:', err);
        updateFeedbackMessage('not-detected', `Unable to access webcam: ${err.message}. Please check browser permissions.`, null);
    }
}

function stopWebcam() {
    if (!isCameraActive || !mediaStream) return;

    mediaStream.getTracks().forEach(track => track.stop());
    mediaStream = null;
    isCameraActive = false;

    const placeholder = document.getElementById('camera-placeholder');
    const liveIndicator = document.getElementById('camera-live-indicator');
    const startBtn = document.getElementById('btn-start-camera');
    const stopBtn = document.getElementById('btn-stop-camera');
    const checkBtn = document.getElementById('btn-check-sign');

    if (videoElement) {
        videoElement.pause();
        videoElement.srcObject = null;
        videoElement.classList.add('d-none');
    }
    if (placeholder) placeholder.classList.remove('d-none');
    if (liveIndicator) liveIndicator.classList.add('d-none');

    // Clear overlay canvas
    if (canvasElement) {
        const ctx = canvasElement.getContext('2d');
        ctx.clearRect(0, 0, canvasElement.width, canvasElement.height);
    }

    if (startBtn) startBtn.classList.remove('d-none');
    if (stopBtn) stopBtn.classList.add('d-none');
    if (checkBtn) checkBtn.disabled = true;
}

async function captureAndRecognize() {
    if (!isCameraActive || isProcessing) return;

    const checkBtn = document.getElementById('btn-check-sign');
    const originalText = checkBtn ? checkBtn.innerHTML : '';
    
    try {
        isProcessing = true;
        if (checkBtn) {
            checkBtn.disabled = true;
            checkBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span> Analyzing Sign...';
        }

        // Draw video frame to hidden canvas
        canvasElement.width = videoElement.videoWidth || 640;
        canvasElement.height = videoElement.videoHeight || 480;
        const ctx = canvasElement.getContext('2d');
        
        // Match mirror orientation
        ctx.save();
        ctx.scale(-1, 1);
        ctx.drawImage(videoElement, -canvasElement.width, 0, canvasElement.width, canvasElement.height);
        ctx.restore();

        const base64Image = canvasElement.toDataURL('image/jpeg', 0.85);

        // Fetch question details from dataset attributes
        const questionContainer = document.getElementById('active-question-card');
        const assignmentId = questionContainer.dataset.assignmentId;
        const questionNum = questionContainer.dataset.questionNum;
        const expectedSign = questionContainer.dataset.expectedSign;

        const response = await fetch('/api/recognize', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                image: base64Image,
                assignment_id: assignmentId,
                question_num: questionNum,
                expected_sign: expectedSign
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Server prediction failed');
        }

        handleRecognitionResult(data, expectedSign);
    } catch (err) {
        console.error('Recognition error:', err);
        updateFeedbackMessage('incorrect', `Recognition error: ${err.message}`, null);
    } finally {
        isProcessing = false;
        if (checkBtn) {
            checkBtn.disabled = false;
            checkBtn.innerHTML = originalText;
        }
    }
}

function handleRecognitionResult(result, expectedSign) {
    const retryBtn = document.getElementById('btn-retry-sign');
    const nextBtn = document.getElementById('btn-next-question');

    if (!result.hand_detected) {
        updateFeedbackMessage(
            'not-detected',
            'Hand not detected! Please ensure your hand is clearly visible in good lighting.',
            null
        );
        return;
    }

    const predicted = result.predicted_sign;
    const confidence = result.confidence;
    const isCorrect = result.is_correct;

    if (isCorrect) {
        updateFeedbackMessage(
            'correct',
            `Correct! Your sign for "${result.expected_sign_name || expectedSign}" is recognized!`,
            { predicted, confidence }
        );

        // Update score badge in header
        if (result.score_info) {
            const scoreDisplay = document.getElementById('assignment-score-display');
            if (scoreDisplay) scoreDisplay.textContent = `${result.score_info.score}%`;
        }

        // Mark active question pill as correct
        const activePill = document.querySelector(`.q-pill[data-qnum="${result.question_num}"]`);
        if (activePill) {
            activePill.classList.remove('active');
            activePill.classList.add('correct');
            activePill.innerHTML = '<i class="bi bi-check-lg"></i>';
        }

        // Show Next button if available
        if (nextBtn) nextBtn.classList.remove('d-none');
        if (retryBtn) retryBtn.classList.add('d-none');

        // Check if assignment complete
        if (result.score_info && result.score_info.status === 'completed') {
            showCompletionModal(result.score_info);
        }
    } else {
        updateFeedbackMessage(
            'incorrect',
            `Not quite! Detected: "${predicted}" (${confidence}% confidence). Try again!`,
            { predicted, confidence }
        );
        if (retryBtn) retryBtn.classList.remove('d-none');
    }
}

function updateFeedbackMessage(type, message, details) {
    const card = document.getElementById('feedback-card');
    const msgEl = document.getElementById('feedback-text');
    const detailsEl = document.getElementById('feedback-details');
    const badgeEl = document.getElementById('feedback-status-badge');

    if (!card || !msgEl) return;

    card.className = 'feedback-card';

    if (type === 'correct') {
        card.classList.add('feedback-correct');
        if (badgeEl) {
            badgeEl.className = 'badge bg-success mb-2';
            badgeEl.innerHTML = '<i class="bi bi-check-circle-fill me-1"></i> Correct';
        }
    } else if (type === 'incorrect') {
        card.classList.add('feedback-incorrect');
        if (badgeEl) {
            badgeEl.className = 'badge bg-danger mb-2';
            badgeEl.innerHTML = '<i class="bi bi-x-circle-fill me-1"></i> Try Again';
        }
    } else if (type === 'not-detected') {
        card.classList.add('feedback-not-detected');
        if (badgeEl) {
            badgeEl.className = 'badge bg-warning text-dark mb-2';
            badgeEl.innerHTML = '<i class="bi bi-exclamation-triangle-fill me-1"></i> No Hand Detected';
        }
    } else {
        card.classList.add('feedback-neutral');
        if (badgeEl) {
            badgeEl.className = 'badge bg-secondary mb-2';
            badgeEl.innerHTML = '<i class="bi bi-info-circle me-1"></i> Ready';
        }
    }

    msgEl.textContent = message;

    if (details && detailsEl) {
        detailsEl.innerHTML = `
            <div class="mt-2 d-flex align-items-center gap-3">
                <span class="small fw-semibold">Predicted: <span class="badge bg-dark">${details.predicted}</span></span>
                <span class="small text-muted">Confidence: <strong>${details.confidence}%</strong></span>
            </div>
            <div class="progress progress-modern mt-1" style="height: 6px;">
                <div class="progress-bar ${type === 'correct' ? 'bg-success' : 'bg-warning'}" style="width: ${details.confidence}%"></div>
            </div>
        `;
        detailsEl.classList.remove('d-none');
    } else if (detailsEl) {
        detailsEl.classList.add('d-none');
    }
}

function resetFeedbackCard() {
    updateFeedbackMessage('neutral', 'Camera active! Hold your hand in position and click "Check Sign".', null);
    const retryBtn = document.getElementById('btn-retry-sign');
    if (retryBtn) retryBtn.classList.add('d-none');
}

function showCompletionModal(scoreInfo) {
    const modalEl = document.getElementById('completionModal');
    if (modalEl && typeof bootstrap !== 'undefined') {
        const modalScore = document.getElementById('modal-final-score');
        const modalCorrect = document.getElementById('modal-correct-count');
        if (modalScore) modalScore.textContent = `${scoreInfo.score}%`;
        if (modalCorrect) modalCorrect.textContent = `${scoreInfo.correct_count} of ${scoreInfo.total}`;

        const modal = new bootstrap.Modal(modalEl);
        modal.show();
    }
}
