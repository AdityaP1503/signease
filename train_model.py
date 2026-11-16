"""
SignEase - Model Training Script
Trains a Random Forest Classifier on hand landmark data for Indian Sign Language signs.
College Mini Project ML Pipeline.
"""

import os
import json
import pickle
import numpy as np
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

BASE_DIR = os.path.dirname(__file__)
DATASET_DIR = os.path.join(BASE_DIR, 'dataset')
MODEL_PATH = os.path.join(BASE_DIR, 'gesture_model.pkl')

SUPPORTED_SIGNS = [
    'HELLO', 'YES', 'NO', 'THANK_YOU',
    '1', '2', '3', '4', '5',
    'C', 'L', 'O'
]

def generate_synthetic_samples_if_needed():
    """
    Generates anatomically consistent starter landmark datasets if dataset directory
    does not have sufficient real collected samples. This ensures the web application
    is 100% functional out-of-the-box for evaluation and presentation.
    """
    os.makedirs(DATASET_DIR, exist_ok=True)

    # Base landmark poses for 21 points (x, y, z)
    # 0: wrist, 1-4: thumb, 5-8: index, 9-12: middle, 13-16: ring, 17-20: pinky
    # In MediaPipe, wrist is at (0, 0, 0). Up is negative y in screen coordinates, or normalized.
    def get_base_pose(sign):
        # Default hand shape template
        # Wrist at (0, 0, 0)
        pose = np.zeros((21, 3), dtype=np.float32)

        # Base finger joints layout at rest
        # Thumb base (MCP, IP, Tip)
        # Index base (MCP, PIP, DIP, Tip)
        # Middle base (MCP, PIP, DIP, Tip)
        # Ring base (MCP, PIP, DIP, Tip)
        # Pinky base (MCP, PIP, DIP, Tip)
        
        # MCP joints relative to wrist
        pose[1] = [-0.12, -0.15, 0.0]   # thumb CMC
        pose[2] = [-0.18, -0.30, 0.0]   # thumb MCP
        pose[5] = [-0.10, -0.45, 0.0]   # index MCP
        pose[9] = [ 0.00, -0.47, 0.0]   # middle MCP
        pose[13] = [ 0.09, -0.45, 0.0]  # ring MCP
        pose[17] = [ 0.17, -0.40, 0.0]  # pinky MCP

        if sign == 'HELLO' or sign == '5':
            # All 5 fingers extended spread
            pose[3] = [-0.25, -0.45, 0.0]
            pose[4] = [-0.32, -0.58, 0.0]   # thumb tip spread
            # Index extended
            pose[6] = [-0.13, -0.62, 0.0]
            pose[7] = [-0.15, -0.76, 0.0]
            pose[8] = [-0.17, -0.90, 0.0]
            # Middle extended
            pose[10] = [0.00, -0.66, 0.0]
            pose[11] = [0.00, -0.82, 0.0]
            pose[12] = [0.00, -0.98, 0.0]
            # Ring extended
            pose[14] = [0.12, -0.63, 0.0]
            pose[15] = [0.14, -0.77, 0.0]
            pose[16] = [0.16, -0.91, 0.0]
            # Pinky extended
            pose[18] = [0.22, -0.54, 0.0]
            pose[19] = [0.26, -0.67, 0.0]
            pose[20] = [0.30, -0.80, 0.0]

        elif sign == 'THANK_YOU':
            # Flat hand with fingers tightly together
            pose[3] = [-0.15, -0.42, 0.02]
            pose[4] = [-0.12, -0.54, 0.02]  # thumb tucked beside
            # Index extended straight
            pose[6] = [-0.07, -0.62, 0.0]
            pose[7] = [-0.07, -0.76, 0.0]
            pose[8] = [-0.07, -0.90, 0.0]
            # Middle extended straight
            pose[10] = [0.00, -0.65, 0.0]
            pose[11] = [0.00, -0.80, 0.0]
            pose[12] = [0.00, -0.95, 0.0]
            # Ring extended straight
            pose[14] = [0.07, -0.62, 0.0]
            pose[15] = [0.07, -0.76, 0.0]
            pose[16] = [0.07, -0.89, 0.0]
            # Pinky extended straight
            pose[18] = [0.14, -0.54, 0.0]
            pose[19] = [0.14, -0.67, 0.0]
            pose[20] = [0.14, -0.79, 0.0]

        elif sign == 'YES':
            # Thumbs Up: Fingers curled into fist, thumb pointing up
            pose[3] = [-0.15, -0.50, 0.05]
            pose[4] = [-0.15, -0.75, 0.08]  # thumb up
            # Index curled
            pose[6] = [-0.08, -0.40, -0.1]
            pose[7] = [-0.05, -0.32, -0.05]
            pose[8] = [-0.04, -0.36, 0.0]
            # Middle curled
            pose[10] = [0.00, -0.41, -0.1]
            pose[11] = [0.00, -0.33, -0.05]
            pose[12] = [0.00, -0.37, 0.0]
            # Ring curled
            pose[14] = [0.08, -0.40, -0.1]
            pose[15] = [0.05, -0.32, -0.05]
            pose[16] = [0.04, -0.36, 0.0]
            # Pinky curled
            pose[18] = [0.15, -0.36, -0.1]
            pose[19] = [0.12, -0.28, -0.05]
            pose[20] = [0.10, -0.32, 0.0]

        elif sign == 'NO' or sign == '1':
            # Index finger straight up, others curled
            pose[3] = [-0.10, -0.32, -0.05]
            pose[4] = [-0.06, -0.34, 0.02]  # thumb across curled fingers
            # Index extended up
            pose[6] = [-0.10, -0.63, 0.0]
            pose[7] = [-0.10, -0.78, 0.0]
            pose[8] = [-0.10, -0.93, 0.0]
            # Middle curled
            pose[10] = [0.00, -0.41, -0.1]
            pose[11] = [0.00, -0.33, -0.05]
            pose[12] = [0.00, -0.37, 0.0]
            # Ring curled
            pose[14] = [0.08, -0.40, -0.1]
            pose[15] = [0.05, -0.32, -0.05]
            pose[16] = [0.04, -0.36, 0.0]
            # Pinky curled
            pose[18] = [0.15, -0.36, -0.1]
            pose[19] = [0.12, -0.28, -0.05]
            pose[20] = [0.10, -0.32, 0.0]

        elif sign == '2':
            # V-sign: Index and Middle extended up separated, others curled
            pose[3] = [-0.08, -0.32, -0.05]
            pose[4] = [-0.04, -0.34, 0.02]  # thumb folded over ring
            # Index extended angled left
            pose[6] = [-0.13, -0.63, 0.0]
            pose[7] = [-0.16, -0.78, 0.0]
            pose[8] = [-0.20, -0.92, 0.0]
            # Middle extended angled right
            pose[10] = [0.06, -0.65, 0.0]
            pose[11] = [0.10, -0.80, 0.0]
            pose[12] = [0.14, -0.95, 0.0]
            # Ring curled
            pose[14] = [0.08, -0.40, -0.1]
            pose[15] = [0.05, -0.32, -0.05]
            pose[16] = [0.04, -0.36, 0.0]
            # Pinky curled
            pose[18] = [0.15, -0.36, -0.1]
            pose[19] = [0.12, -0.28, -0.05]
            pose[20] = [0.10, -0.32, 0.0]

        elif sign == '3':
            # Index, Middle, Ring extended, pinky curled
            pose[3] = [-0.08, -0.32, -0.05]
            pose[4] = [0.06, -0.32, 0.02]   # thumb folded over pinky
            # Index extended
            pose[6] = [-0.14, -0.63, 0.0]
            pose[7] = [-0.16, -0.78, 0.0]
            pose[8] = [-0.18, -0.92, 0.0]
            # Middle extended
            pose[10] = [0.00, -0.65, 0.0]
            pose[11] = [0.00, -0.80, 0.0]
            pose[12] = [0.00, -0.95, 0.0]
            # Ring extended
            pose[14] = [0.12, -0.63, 0.0]
            pose[15] = [0.14, -0.78, 0.0]
            pose[16] = [0.16, -0.91, 0.0]
            # Pinky curled
            pose[18] = [0.15, -0.36, -0.1]
            pose[19] = [0.12, -0.28, -0.05]
            pose[20] = [0.10, -0.32, 0.0]

        elif sign == '4':
            # 4 fingers extended, thumb folded across palm
            pose[3] = [-0.05, -0.30, -0.05]
            pose[4] = [0.02, -0.32, 0.02]   # thumb folded inside palm
            # Index extended
            pose[6] = [-0.10, -0.63, 0.0]
            pose[7] = [-0.10, -0.78, 0.0]
            pose[8] = [-0.10, -0.92, 0.0]
            # Middle extended
            pose[10] = [0.00, -0.65, 0.0]
            pose[11] = [0.00, -0.80, 0.0]
            pose[12] = [0.00, -0.95, 0.0]
            # Ring extended
            pose[14] = [0.09, -0.63, 0.0]
            pose[15] = [0.09, -0.78, 0.0]
            pose[16] = [0.09, -0.91, 0.0]
            # Pinky extended
            pose[18] = [0.17, -0.55, 0.0]
            pose[19] = [0.17, -0.68, 0.0]
            pose[20] = [0.17, -0.81, 0.0]

        elif sign == 'C':
            # Curved C handshape
            pose[3] = [-0.22, -0.35, 0.0]
            pose[4] = [-0.18, -0.48, 0.0]
            # Index curved
            pose[6] = [-0.15, -0.60, 0.0]
            pose[7] = [-0.08, -0.66, 0.0]
            pose[8] = [0.02, -0.63, 0.0]
            # Middle curved
            pose[10] = [-0.05, -0.62, 0.0]
            pose[11] = [0.02, -0.67, 0.0]
            pose[12] = [0.11, -0.64, 0.0]
            # Ring curved
            pose[14] = [0.04, -0.60, 0.0]
            pose[15] = [0.10, -0.65, 0.0]
            pose[16] = [0.18, -0.62, 0.0]
            # Pinky curved
            pose[18] = [0.12, -0.52, 0.0]
            pose[19] = [0.17, -0.57, 0.0]
            pose[20] = [0.23, -0.54, 0.0]

        elif sign == 'L':
            # Index up, thumb 90 deg out, others curled
            pose[3] = [-0.25, -0.30, 0.0]
            pose[4] = [-0.38, -0.30, 0.0]  # thumb pointing horizontal left
            # Index straight up
            pose[6] = [-0.10, -0.63, 0.0]
            pose[7] = [-0.10, -0.78, 0.0]
            pose[8] = [-0.10, -0.93, 0.0]
            # Middle curled
            pose[10] = [0.00, -0.41, -0.1]
            pose[11] = [0.00, -0.33, -0.05]
            pose[12] = [0.00, -0.37, 0.0]
            # Ring curled
            pose[14] = [0.08, -0.40, -0.1]
            pose[15] = [0.05, -0.32, -0.05]
            pose[16] = [0.04, -0.36, 0.0]
            # Pinky curled
            pose[18] = [0.15, -0.36, -0.1]
            pose[19] = [0.12, -0.28, -0.05]
            pose[20] = [0.10, -0.32, 0.0]

        elif sign == 'O':
            # Fingertips touch thumb tip forming circle
            pose[3] = [-0.15, -0.45, 0.0]
            pose[4] = [-0.05, -0.52, 0.0]  # thumb tip
            # All fingertips converge near (-0.05, -0.52)
            pose[6] = [-0.12, -0.60, 0.0]
            pose[7] = [-0.08, -0.57, 0.0]
            pose[8] = [-0.05, -0.52, 0.0]
            # Middle
            pose[10] = [-0.02, -0.61, 0.0]
            pose[11] = [-0.04, -0.57, 0.0]
            pose[12] = [-0.05, -0.52, 0.0]
            # Ring
            pose[14] = [0.05, -0.59, 0.0]
            pose[15] = [0.00, -0.56, 0.0]
            pose[16] = [-0.04, -0.52, 0.0]
            # Pinky
            pose[18] = [0.10, -0.53, 0.0]
            pose[19] = [0.04, -0.53, 0.0]
            pose[20] = [-0.03, -0.51, 0.0]

        return pose

    for sign in SUPPORTED_SIGNS:
        filepath = os.path.join(DATASET_DIR, f"{sign}.json")
        if os.path.exists(filepath):
            continue

        base = get_base_pose(sign)
        samples = []

        # Generate 150 variations per sign with realistic variations
        for _ in range(150):
            # 1. Random 3D Rotation (Roll, Pitch, Yaw)
            angle_z = np.random.normal(0, np.radians(7))  # in-plane tilt
            angle_x = np.random.normal(0, np.radians(6))  # pitch
            angle_y = np.random.normal(0, np.radians(6))  # yaw

            # Rotation matrices
            Rx = np.array([
                [1, 0, 0],
                [0, np.cos(angle_x), -np.sin(angle_x)],
                [0, np.sin(angle_x), np.cos(angle_x)]
            ])
            Ry = np.array([
                [np.cos(angle_y), 0, np.sin(angle_y)],
                [0, 1, 0],
                [-np.sin(angle_y), 0, np.cos(angle_y)]
            ])
            Rz = np.array([
                [np.cos(angle_z), -np.sin(angle_z), 0],
                [np.sin(angle_z), np.cos(angle_z), 0],
                [0, 0, 1]
            ])
            R = Rz @ Ry @ Rx

            # Rotate pose
            rotated = base @ R.T

            # 2. Add realistic joint jitter / slight natural variations
            jitter = np.random.normal(0, 0.015, rotated.shape)
            # Wrist stays fixed at (0,0,0)
            jitter[0] = 0.0
            varied = rotated + jitter

            # 3. Scale normalization matching ml_utils.extract_features
            dists = np.linalg.norm(varied, axis=1)
            max_d = np.max(dists)
            if max_d < 1e-6:
                max_d = 1.0
            normalized = varied / max_d

            # Flatten to 63 features
            features = normalized.flatten().tolist()
            samples.append(features)

        with open(filepath, 'w') as f:
            json.dump(samples, f)
        print(f"[Dataset] Generated {len(samples)} baseline samples for {sign}")

def train():
    print("=" * 50)
    print("SignEase - Indian Sign Language Model Training")
    print("=" * 50)

    generate_synthetic_samples_if_needed()

    X = []
    y = []

    for filename in os.listdir(DATASET_DIR):
        if not filename.endswith('.json'):
            continue
        sign_code = os.path.splitext(filename)[0]
        filepath = os.path.join(DATASET_DIR, filename)
        try:
            with open(filepath, 'r') as f:
                samples = json.load(f)
                for sample in samples:
                    if len(sample) == 63:
                        X.append(sample)
                        y.append(sign_code)
        except Exception as e:
            print(f"[!] Error loading {filename}: {e}")

    X = np.array(X, dtype=np.float32)
    y = np.array(y)

    print(f"\n[Info] Total samples loaded: {len(X)}")
    unique_classes, counts = np.unique(y, return_counts=True)
    for cls, count in zip(unique_classes, counts):
        print(f"  - {cls:<12}: {count} samples")

    if len(unique_classes) < 2:
        print("[Error] Not enough classes to train model. Need at least 2.")
        return

    # Train / Test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print(f"\n[Info] Training Random Forest Classifier...")
    clf = RandomForestClassifier(
        n_estimators=120,
        max_depth=16,
        min_samples_split=2,
        random_state=42,
        n_jobs=-1
    )
    clf.fit(X_train, y_train)

    # Evaluate
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\n[Evaluation Result]")
    print(f"Model Accuracy on Test Set: {accuracy * 100:.2f}%\n")
    print(classification_report(y_test, y_pred, digits=3))

    # Save model bundle
    bundle = {
        'model': clf,
        'classes': list(clf.classes_),
        'feature_count': X.shape[1],
        'accuracy': float(accuracy),
        'trained_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(bundle, f)

    print(f"[Success] Trained model saved to: {MODEL_PATH}")
    print("=" * 50)

if __name__ == '__main__':
    train()
