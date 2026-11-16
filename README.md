# SignEase – Indian Sign Language (ISL) Learning Platform

> **Third-Year College Mini Project**  
> *Tagline:* **Learn Signs, Connect Hearts.**  
> An interactive, beginner-friendly web application designed to help hearing and hard-of-hearing individuals learn Indian Sign Language with real-time AI webcam feedback.

---

## 📌 Project Overview

SignEase bridges the communication barrier between hearing and hard-of-hearing individuals by providing:
1. **Interactive Curriculum:** Structured lessons across **Basic Words**, **Numbers (0–9)**, and **Alphabets** with accurate ISL reference diagrams and plain-language movement tips.
2. **Practical Daily Assignment:** 5 daily rotated questions where learners perform signs in front of their webcam.
3. **Real-time AI Verification:** MediaPipe detects the hand, extracts 21 spatial landmarks with wrist-relative scale normalization, and a Scikit-learn Random Forest classifier predicts the gesture in real-time.
4. **Instant Feedback & Scoring:** Instant notifications (*"Correct! Your sign is recognized"*, *"Not quite! Try again"*, or *"Hand not detected"*), confidence score, and persistent SQLite tracking.
5. **My Progress Analytics:** Visual dashboard displaying total completed assignments, attempted signs, correct vs. incorrect gestures, and overall accuracy percentage.

---

## 🛠️ Technology Stack

| Component | Technology | Description |
|---|---|---|
| **Frontend** | HTML5, CSS3, JavaScript (ES6), Bootstrap 5 | Responsive UI, soft blue/purple modern light theme |
| **Backend** | Python Flask | Lightweight RESTful web server and API routes |
| **Database** | SQLite (`signease.db`) | Embedded database storing lessons, daily assignments & scores |
| **Computer Vision** | OpenCV (`cv2`) | Frame decoding, image processing and annotation overlay |
| **Hand Tracking** | Google MediaPipe | Real-time detection of 21 3D hand landmarks |
| **Machine Learning** | Scikit-learn Random Forest | Fast, multi-class ensemble classification of normalized landmark coordinates |

---

## 📁 Project Structure

```text
SignEase/
│
├── app.py                  # Flask web server and API endpoints (/api/recognize)
├── models.py               # SQLite database schemas, queries, and daily rotation logic
├── ml_utils.py             # MediaPipe 21 landmark extraction & scale-invariant normalization
├── train_model.py          # Random Forest ML model training and evaluation script
├── collect_data.py         # Interactive OpenCV camera tool to record custom gesture samples
├── gesture_model.pkl       # Trained ML model bundle with class labels and metadata
├── requirements.txt        # Project Python dependencies
├── README.md               # Complete project documentation and guide
│
├── dataset/                # Hand landmark JSON samples per supported sign
│   ├── HELLO.json
│   ├── YES.json
│   ├── NO.json
│   ├── THANK_YOU.json
│   ├── 1.json, 2.json, 3.json, 4.json, 5.json
│   └── C.json, L.json, O.json
│
├── static/
│   ├── css/
│   │   └── style.css       # Custom modern light theme stylesheet
│   ├── js/
│   │   └── assignment.js   # Webcam stream controller and client-side recognition calls
│   └── images/
│       └── signs/          # Clean SVG reference illustrations for ISL signs
│
└── templates/
    ├── base.html           # Master navigation bar and layout template
    ├── index.html          # Home landing page with 3 feature cards & ISL intro
    ├── learn.html          # Curriculum catalog with category filter pills
    ├── lesson.html         # Detailed sign guide with single-sign camera practice
    ├── assignment.html     # Daily assignment interface (Question left, Camera right)
    └── progress.html       # Analytics dashboard with accuracy formula and history table
```

---

## 🧠 How the AI Recognition Pipeline Works

```text
Browser Webcam (getUserMedia)
           │
           ▼
HTML5 Canvas (Base64 JPEG Capture)
           │
           ▼  POST /api/recognize
Flask Backend (app.py)
           │
           ▼
OpenCV Frame Decoding (cv2)
           │
           ▼
MediaPipe Hand Tracking (mp.solutions.hands)
           │
           ├── Hand Detected? ──> NO ──> Return "Hand not detected"
           │
           ▼ YES (21 Spatial Landmarks)
Feature Extraction & Normalization:
  1. Wrist-relative translation: (x_i - x_0, y_i - y_0, z_i - z_0)
  2. Scale normalization: max Euclidean distance = 1.0 (Distance-invariant)
           │
           ▼
Random Forest Classifier (gesture_model.pkl)
           │
           ▼
Predicted Sign & Confidence (%)
           │
           ▼
Match Check (Predicted Sign == Expected Question Sign?)
           │
           ▼
Update SQLite Daily Assignment Score & Return Result to Browser
```

---

## 🚀 Quick Setup & Installation

### Step 1: Clone or Navigate to the Project Directory
```powershell
cd SignEase
```

### Step 2: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 3: Train the Gesture Recognition Model (Optional - Pre-trained model included)
```powershell
python train_model.py
```

### Step 4: Run the Flask Web Application
```powershell
python app.py
```

### Step 5: Open in Your Browser
Visit: **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 🎓 College Presentation Q&A Reference

1. **Why use MediaPipe instead of raw CNN image pixels?**
   - Raw image pixels are sensitive to background clutter, lighting conditions, and skin tones. MediaPipe extracts skeletal landmarks that isolate *pure hand geometry*, enabling lightweight, ultra-fast and robust classification with zero GPU requirements.
2. **Why Random Forest for classification?**
   - Random Forest is an ensemble of decision trees. It excels with structured tabular landmark features (63 normalized coordinates), trains in seconds, prevents overfitting, and outputs transparent prediction probabilities (confidence scores).
3. **How does normalization achieve distance-invariance?**
   - Landmark coordinates are subtracted from the wrist position and divided by the maximum joint distance. Whether the user stands close to or far from the camera, the normalized feature vector remains identical.
4. **How does Daily Assignment Rotation work?**
   - The date string (`YYYY-MM-DD`) is passed through a deterministic MD5 hash seed to rotate 5 varied signs each day, ensuring fresh daily practice without duplicate sets.
