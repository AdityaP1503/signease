import os
import io
import base64
import pickle
import numpy as np
import cv2
from PIL import Image

try:
    import mediapipe as mp
    if hasattr(mp, 'solutions'):
        mp_hands = mp.solutions.hands
        mp_drawing = mp.solutions.drawing_utils
        mp_drawing_styles = mp.solutions.drawing_styles
        MEDIAPIPE_AVAILABLE = True
    else:
        try:
            from mediapipe.python.solutions import hands as mp_hands
            from mediapipe.python.solutions import drawing_utils as mp_drawing
            from mediapipe.python.solutions import drawing_styles as mp_drawing_styles
            MEDIAPIPE_AVAILABLE = True
        except ImportError:
            MEDIAPIPE_AVAILABLE = False
            mp_hands = None
            mp_drawing = None
            mp_drawing_styles = None
except Exception:
    MEDIAPIPE_AVAILABLE = False
    mp_hands = None
    mp_drawing = None
    mp_drawing_styles = None

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'gesture_model.pkl')

# Global detector instance for fast reuse
_hands_detector = None

def get_hands_detector():
    global _hands_detector
    if _hands_detector is None and MEDIAPIPE_AVAILABLE:
        _hands_detector = mp_hands.Hands(
            static_image_mode=True,
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
    return _hands_detector

def extract_features(hand_landmarks):
    """
    Extracts 63 scale-invariant, wrist-relative landmark features:
    (dx_i / scale, dy_i / scale, dz_i / scale) for i = 0..20
    """
    # Landmark 0 is wrist
    wrist_x = hand_landmarks.landmark[0].x
    wrist_y = hand_landmarks.landmark[0].y
    wrist_z = hand_landmarks.landmark[0].z

    coords = []
    distances = []

    for lm in hand_landmarks.landmark:
        dx = lm.x - wrist_x
        dy = lm.y - wrist_y
        dz = lm.z - wrist_z
        coords.append((dx, dy, dz))
        distances.append(np.sqrt(dx**2 + dy**2 + dz**2))

    max_dist = max(distances)
    if max_dist < 1e-6:
        max_dist = 1.0

    features = []
    for dx, dy, dz in coords:
        features.extend([dx / max_dist, dy / max_dist, dz / max_dist])

    return np.array(features, dtype=np.float32)

def decode_base64_image(b64_string):
    """Decodes data URL or raw base64 string to an OpenCV BGR image."""
    if ',' in b64_string:
        b64_string = b64_string.split(',')[1]
    image_bytes = base64.b64decode(b64_string)
    image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    frame_bgr = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    return frame_bgr

def encode_image_base64(b64_image_bgr):
    """Encodes an OpenCV BGR image to base64 JPEG data URL."""
    _, buffer = cv2.imencode('.jpg', b64_image_bgr, [cv2.IMWRITE_JPEG_QUALITY, 85])
    b64 = base64.b64encode(buffer).decode('utf-8')
    return f"data:image/jpeg;base64,{b64}"

def detect_hand_and_extract(frame_bgr, draw_landmarks=True):
    """
    Processes a frame with MediaPipe, draws landmarks if requested,
    and returns (features, annotated_frame_bgr, landmark_coords).
    Returns (None, frame_bgr, None) if no hand is detected.
    """
    detector = get_hands_detector()
    if detector is None:
        return None, frame_bgr, None

    frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    results = detector.process(frame_rgb)

    if not results.multi_hand_landmarks:
        return None, frame_bgr, None

    # Use primary detected hand
    hand_landmarks = results.multi_hand_landmarks[0]
    features = extract_features(hand_landmarks)

    annotated_frame = frame_bgr.copy()
    if draw_landmarks and mp_drawing:
        mp_drawing.draw_landmarks(
            annotated_frame,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style()
        )

    # Return key landmarks for client preview if needed
    raw_landmarks = [{'x': lm.x, 'y': lm.y, 'z': lm.z} for lm in hand_landmarks.landmark]

    return features, annotated_frame, raw_landmarks

def load_gesture_model(path=MODEL_PATH):
    """Loads the trained model bundle containing the classifier and label mappings."""
    if not os.path.exists(path):
        return None
    try:
        with open(path, 'rb') as f:
            data = pickle.load(f)
            return data
    except Exception as e:
        print(f"Error loading model from {path}: {e}")
        return None

def predict_sign(model_bundle, features):
    """
    Predicts gesture and returns (predicted_label, confidence_score_float).
    """
    if model_bundle is None or features is None:
        return None, 0.0

    clf = model_bundle['model']
    classes = model_bundle['classes']

    features_reshaped = features.reshape(1, -1)
    probabilities = clf.predict_proba(features_reshaped)[0]
    best_idx = np.argmax(probabilities)
    predicted_label = str(classes[best_idx])
    confidence = float(probabilities[best_idx])

    return predicted_label, round(confidence * 100, 1)
