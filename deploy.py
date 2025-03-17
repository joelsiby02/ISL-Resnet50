# deploy.py
import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

import streamlit as st
import requests
import os
import atexit
import shutil
from flask import Flask, request, jsonify, send_from_directory
from ultralytics import YOLO
import threading
import cv2
import glob
from streamlit_extras.let_it_rain import rain

# ---------------------- Flask Backend Setup ----------------------
app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
RESULT_FOLDER = "runs/detect/predict"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

# Load YOLO model
MODEL_PATH = "my_model.pt"
model = YOLO(MODEL_PATH).to('cpu')  # Force CPU device

def convert_video_to_mp4(input_path, output_path):
    cap = cv2.VideoCapture(input_path)
    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    out = cv2.VideoWriter(output_path, fourcc, 
                         cap.get(cv2.CAP_PROP_FPS), 
                         (int(cap.get(3)), int(cap.get(4))))
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
        out.write(frame)
    cap.release()
    out.release()
    os.remove(input_path)

@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files["file"]
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    model.predict(source=file_path, save=True, project="runs/detect", name="predict", exist_ok=True)
    result_path = os.path.join(RESULT_FOLDER, file.filename)
    return jsonify({"result_image": f"/results/{file.filename}"})

@app.route("/predict_video", methods=["POST"])
def predict_video():
    file = request.files["file"]
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    detected_classes = set()
    results = model.predict(source=file_path, save=True, project="runs/detect", name="predict", exist_ok=True)
    for result in results:
        for box in result.boxes:
            detected_classes.add(model.names[int(box.cls.item())])
    base_name = os.path.splitext(file.filename)[0]
    avi_path = max(glob.glob(os.path.join(RESULT_FOLDER, f"{base_name}*.avi")), key=os.path.getctime)
    mp4_path = avi_path.replace(".avi", ".mp4")
    convert_video_to_mp4(avi_path, mp4_path)
    return jsonify({"result_video": f"/results/{os.path.basename(mp4_path)}", "detected_classes": list(detected_classes)})

@app.route("/results/<filename>")
def get_result_file(filename):
    return send_from_directory(RESULT_FOLDER, filename)

def run_flask():
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

# Start Flask in background thread
flask_thread = threading.Thread(target=run_flask)
flask_thread.daemon = True
flask_thread.start()

# ---------------------- Streamlit Frontend ----------------------
# Configuration
API_URL = "http://localhost:5000/predict"
ALLOWED_IMAGE_TYPES = ["jpg", "jpeg", "png"]
ALLOWED_VIDEO_TYPES = ["mp4", "avi", "mov"]

# Cleanup function
def cleanup():
    if os.path.exists("temp"):
        shutil.rmtree("temp", ignore_errors=True)
atexit.register(cleanup)

# UI Configuration
st.set_page_config(
    page_title="ISL Detector",
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS and sidebar setup
st.markdown("""
    <style>
    .main { background: #f8f9fa; }
    .stButton>button { background: #4a90e2; color: white; border-radius: 8px; }
    .result-box { border: 2px solid #e0e0e0; border-radius: 10px; padding: 1rem; }
    </style>""", unsafe_allow_html=True)

with st.sidebar:
    st.title("🖼️ ISL Detection System")
    app_mode = st.radio("Select Mode", ["📷 Image Detection", "🎥 Video Analysis", "📸 Live Capture"])
    st.markdown("---")
    with st.expander("ℹ️ Instructions"):
        st.markdown("""1. Select mode\n2. Upload media\n3. Detect objects""")

# Main application logic
def success_animation():
    rain(emoji="🎉", font_size=20, falling_speed=3, animation_length=1)

def handle_image():
    uploaded_file = st.file_uploader("Upload image", type=ALLOWED_IMAGE_TYPES)
    if uploaded_file and st.button("🔍 Detect Objects"):
        with st.spinner("Analyzing..."):
            response = requests.post(API_URL, files={"file": uploaded_file})
            if response.status_code == 200:
                result = response.json()
                col1, col2 = st.columns(2)
                with col1: st.image(uploaded_file, use_container_width=True)
                with col2: 
                    st.image(f"http://localhost:5000/results/{uploaded_file.name}", 
                            use_container_width=True)
                    success_animation()

def handle_video():
    uploaded_video = st.file_uploader("Upload video", type=ALLOWED_VIDEO_TYPES)
    if uploaded_video and st.button("🔍 Analyze Video"):
        with st.spinner("Processing..."):
            response = requests.post("http://localhost:5000/predict_video", files={"file": uploaded_video})
            if response.status_code == 200:
                result = response.json()
                st.video(f"http://localhost:5000/results/{result['result_video'].split('/')[-1]}")

def handle_camera():
    frame = st.camera_input("Take a picture")
    if frame and st.button("🔍 Detect"):
        with st.spinner("Processing..."):
            response = requests.post("http://localhost:5000/predict_frame", files={"file": frame})
            if response.status_code == 200:
                result = response.json()
                col1, col2 = st.columns(2)
                with col1: st.image(frame, use_container_width=True)
                with col2: st.image(f"http://localhost:5000/results/{result['result_image'].split('/')[-1]}")

# Routing
st.title("ISL - Resnet 50 / YOLO V11")
if "Image" in app_mode: handle_image()
elif "Video" in app_mode: handle_video()
else: handle_camera()

# Footer
st.markdown("---")
st.markdown("🚀 Powered by Diya Group | 🔐 Secure Processing", unsafe_allow_html=True)
