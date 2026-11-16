"""
SignEase - Dataset Collection Script
Collects hand landmark samples using OpenCV and MediaPipe for Indian Sign Language signs.
College Mini Project Utility.
"""

import os
import time
import json
import argparse
import numpy as np
import cv2
from ml_utils import get_hands_detector, extract_features

DATASET_DIR = os.path.join(os.path.dirname(__file__), 'dataset')
os.makedirs(DATASET_DIR, exist_ok=True)

SUPPORTED_SIGNS = [
    'HELLO', 'YES', 'NO', 'THANK_YOU',
    '1', '2', '3', '4', '5',
    'C', 'L', 'O'
]

def collect_for_sign(sign_name, num_samples=60, camera_index=0):
    sign_name = sign_name.upper().strip()
    if sign_name not in SUPPORTED_SIGNS:
        print(f"[!] Warning: '{sign_name}' is not in default list, but will still be saved.")

    print(f"\n==========================================")
    print(f" Collecting data for sign: {sign_name}")
    print(f" Target samples: {num_samples}")
    print(f" Press 's' to START recording when your hand is in position.")
    print(f" Press 'q' to QUIT without saving.")
    print(f"==========================================\n")

    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print(f"[Error] Could not open webcam (index {camera_index}). Check camera connection.")
        return

    detector = get_hands_detector()
    collected_features = []
    is_recording = False
    countdown = 3
    start_time = None

    from ml_utils import mp_hands, mp_drawing
    mp_draw = mp_drawing

    while cap.isOpened() and len(collected_features) < num_samples:
        ret, frame = cap.read()
        if not ret:
            break

        # Flip horizontally for natural mirror feel
        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = detector.process(rgb)

        hand_detected = False
        if results.multi_hand_landmarks:
            hand_detected = True
            for hand_lms in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_lms, mp_hands.HAND_CONNECTIONS)

        # Header bar
        cv2.rectangle(frame, (0, 0), (w, 60), (30, 30, 30), -1)
        status_text = f"Sign: {sign_name} | Collected: {len(collected_features)}/{num_samples}"
        cv2.putText(frame, status_text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 200), 2)

        # Bottom guidance
        cv2.rectangle(frame, (0, h - 50), (w, h), (30, 30, 30), -1)

        if not is_recording:
            cv2.putText(frame, "Press 's' to start countdown | 'q' to cancel", (20, h - 18),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        else:
            elapsed = time.time() - start_time
            if elapsed < countdown:
                rem = countdown - int(elapsed)
                cv2.putText(frame, f"Starting in: {rem}...", (w // 2 - 100, h // 2),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 165, 255), 3)
            else:
                cv2.putText(frame, "RECORDING... Shift hand slightly for variation", (20, h - 18),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                if hand_detected:
                    features = extract_features(results.multi_hand_landmarks[0])
                    collected_features.append(features.tolist())
                    time.sleep(0.04)  # Small delay to capture slightly different frames

        cv2.imshow("SignEase - Dataset Collector", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            print("Cancelled by user.")
            break
        elif key == ord('s') and not is_recording:
            is_recording = True
            start_time = time.time()

    cap.release()
    cv2.destroyAllWindows()

    if len(collected_features) > 0:
        output_file = os.path.join(DATASET_DIR, f"{sign_name}.json")
        existing_data = []
        if os.path.exists(output_file):
            try:
                with open(output_file, 'r') as f:
                    existing_data = json.load(f)
            except Exception:
                existing_data = []

        combined = existing_data + collected_features
        with open(output_file, 'w') as f:
            json.dump(combined, f)

        print(f"[Success] Saved {len(collected_features)} new samples (Total: {len(combined)}) to {output_file}")
    else:
        print("[!] No samples were saved.")

def main():
    parser = argparse.ArgumentParser(description="SignEase Landmark Dataset Collector")
    parser.add_argument("--sign", type=str, default=None, help="Sign name to collect (e.g. HELLO, YES, 1, C)")
    parser.add_argument("--samples", type=int, default=60, help="Number of samples to collect (default: 60)")
    parser.add_argument("--camera", type=int, default=0, help="Camera device index (default: 0)")
    args = parser.parse_args()

    if args.sign:
        collect_for_sign(args.sign, args.samples, args.camera)
    else:
        print("Available Supported Signs:")
        for idx, s in enumerate(SUPPORTED_SIGNS, 1):
            print(f" {idx}. {s}")
        choice = input("\nEnter sign name or number to collect (or 'q' to quit): ").strip()
        if choice.lower() == 'q':
            return
        if choice.isdigit() and 1 <= int(choice) <= len(SUPPORTED_SIGNS):
            selected_sign = SUPPORTED_SIGNS[int(choice) - 1]
        else:
            selected_sign = choice.upper()
        collect_for_sign(selected_sign, args.samples, args.camera)

if __name__ == '__main__':
    main()
