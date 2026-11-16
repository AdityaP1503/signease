"""
SignEase - Indian Sign Language Learning Platform
Flask Web Application Backend
"""

import os
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash

from models import (
    init_db,
    get_lessons,
    get_lesson_by_code,
    get_supported_ml_signs,
    get_or_create_daily_assignment,
    update_question_result,
    get_progress_summary
)
from ml_utils import (
    decode_base64_image,
    detect_hand_and_extract,
    load_gesture_model,
    predict_sign,
    encode_image_base64
)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'signease_secret_key_college_proj_2026')

# Initialize database
init_db()

# Load trained Random Forest model bundle
model_bundle = load_gesture_model()

@app.route('/')
def index():
    supported_signs = get_supported_ml_signs()
    return render_template('index.html', supported_signs=supported_signs)

@app.route('/learn')
def learn():
    category = request.args.get('category')
    lessons = get_lessons(category=category)
    return render_template('learn.html', lessons=lessons, active_category=category)

@app.route('/lesson/<sign_code>')
def lesson_detail(sign_code):
    lesson = get_lesson_by_code(sign_code.upper())
    if not lesson:
        flash(f"Sign '{sign_code}' not found.", "warning")
        return redirect(url_for('learn'))
    return render_template('lesson.html', lesson=dict(lesson))

@app.route('/assignment')
def assignment():
    date_str = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
    q_num = request.args.get('q', 1, type=int)

    assignment_data, questions = get_or_create_daily_assignment(date_str)
    
    # If a specific sign code was requested via ?sign=XYZ, jump to that question if present
    target_sign = request.args.get('sign')
    if target_sign:
        for idx, q in enumerate(questions, 1):
            if q['sign_code'].upper() == target_sign.upper():
                q_num = idx
                break

    # Bound q_num within questions range
    if q_num < 1:
        q_num = 1
    elif q_num > len(questions):
        q_num = len(questions)

    current_q = questions[q_num - 1]

    return render_template(
        'assignment.html',
        assignment=assignment_data,
        questions=questions,
        current_q=current_q
    )

@app.route('/progress')
def progress():
    summary = get_progress_summary()
    return render_template('progress.html', summary=summary)

@app.route('/api/recognize', methods=['POST'])
def recognize_gesture():
    global model_bundle
    if model_bundle is None:
        # Attempt to reload if trained recently
        model_bundle = load_gesture_model()

    data = request.get_json(silent=True) or {}
    b64_image = data.get('image')
    assignment_id = int(data.get('assignment_id', 0))
    question_num = int(data.get('question_num', 1))
    expected_sign = str(data.get('expected_sign', '')).upper().strip()

    if not b64_image:
        return jsonify({'error': 'No image data provided.'}), 400

    try:
        frame_bgr = decode_base64_image(b64_image)
    except Exception as e:
        return jsonify({'error': f'Failed to process image frame: {str(e)}'}), 400

    # Extract 21 hand landmarks and normalized relative features
    features, annotated_frame, _ = detect_hand_and_extract(frame_bgr, draw_landmarks=True)

    if features is None:
        return jsonify({
            'hand_detected': False,
            'message': 'Hand not detected. Please show your hand clearly in front of the camera.'
        })

    # Predict using Random Forest
    if model_bundle is None:
        return jsonify({
            'hand_detected': True,
            'error': 'ML model has not been trained yet. Please run train_model.py first.',
            'predicted_sign': None,
            'confidence': 0.0,
            'is_correct': False
        }), 503

    predicted_sign, confidence = predict_sign(model_bundle, features)

    # Evaluate correctness against expected sign
    # Note: 1 and NO, or 2 and V, share equivalent handshapes in static ISL
    is_correct = False
    if predicted_sign == expected_sign:
        is_correct = True
    elif expected_sign == '1' and predicted_sign == 'NO':
        is_correct = True
    elif expected_sign == 'NO' and predicted_sign == '1':
        is_correct = True
    elif expected_sign == '2' and predicted_sign == 'V':
        is_correct = True
    elif expected_sign == 'HELLO' and predicted_sign == '5':
        is_correct = True
    elif expected_sign == '5' and predicted_sign == 'HELLO':
        is_correct = True

    # Update database record if this is a daily assignment question
    score_info = None
    if assignment_id > 0:
        score_info = update_question_result(
            assignment_id=assignment_id,
            question_num=question_num,
            predicted_sign=predicted_sign,
            confidence=confidence,
            is_correct=is_correct
        )

    lesson_info = get_lesson_by_code(expected_sign)
    expected_name = lesson_info['name'] if lesson_info else expected_sign

    return jsonify({
        'hand_detected': True,
        'predicted_sign': predicted_sign,
        'confidence': confidence,
        'is_correct': is_correct,
        'expected_sign': expected_sign,
        'expected_sign_name': expected_name,
        'question_num': question_num,
        'score_info': score_info
    })

@app.route('/api/model-status')
def model_status():
    global model_bundle
    if model_bundle is None:
        model_bundle = load_gesture_model()

    if model_bundle is None:
        return jsonify({
            'status': 'not_trained',
            'message': 'Model file gesture_model.pkl not found. Run python train_model.py.'
        })

    return jsonify({
        'status': 'ready',
        'classes': model_bundle.get('classes', []),
        'accuracy': model_bundle.get('accuracy', 0.0),
        'trained_at': model_bundle.get('trained_at', '')
    })

if __name__ == '__main__':
    print("\n" + "=" * 50)
    print("SignEase – Indian Sign Language Platform Starting")
    print("Local URL: http://127.0.0.1:5000")
    print("=" * 50 + "\n")
    app.run(host='127.0.0.1', port=5000, debug=True)
