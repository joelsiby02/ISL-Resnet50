import os
import tempfile
import shutil
import cv2
import glob
import subprocess
import streamlit as st
from ultralytics import YOLO
from streamlit_extras.let_it_rain import rain

# ---------------------- Configuration ----------------------
st.set_page_config(
    page_title="ISL Detector",
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize model
MODEL_PATH = "my_model.pt"
model = YOLO(MODEL_PATH).to('cpu')  # Force CPU usage

# Temporary directories
UPLOAD_FOLDER = tempfile.gettempdir()
RESULT_FOLDER = tempfile.gettempdir()
ALLOWED_IMAGE_TYPES = ["jpg", "jpeg", "png"]
ALLOWED_VIDEO_TYPES = ["mp4", "avi", "mov"]

# ---------------------- Helper Functions ----------------------
def success_animation():
    rain(emoji="🎉", font_size=20, falling_speed=3, animation_length=1)

def cleanup():
    for folder in [UPLOAD_FOLDER, RESULT_FOLDER]:
        if os.path.exists(folder):
            shutil.rmtree(folder, ignore_errors=True)
    if os.path.exists("runs"):
        shutil.rmtree("runs", ignore_errors=True)

atexit.register(cleanup)

def convert_video_to_mp4(input_path, output_path):
    """Convert video using FFmpeg"""
    try:
        subprocess.run([
            'ffmpeg', '-i', input_path,
            '-vcodec', 'libx264',
            output_path, '-y'
        ], check=True)
        os.remove(input_path)
        return True
    except Exception as e:
        st.error(f"Video conversion failed: {str(e)}")
        return False

# ---------------------- Prediction Handlers ----------------------
def predict_image(uploaded_file):
    """Handle image prediction"""
    try:
        # Save uploaded file
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Run prediction
        results = model.predict(
            source=file_path,
            save=True,
            project=RESULT_FOLDER,
            name="predict",
            exist_ok=True
        )
        
        # Get result path
        result_dir = os.path.join(RESULT_FOLDER, "predict")
        return glob.glob(os.path.join(result_dir, uploaded_file.name))[0]
        
    except Exception as e:
        st.error(f"Image prediction failed: {str(e)}")
        return None

def predict_video(uploaded_file):
    """Handle video prediction"""
    try:
        # Save uploaded file
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Run prediction
        results = model.predict(
            source=file_path,
            save=True,
            project=RESULT_FOLDER,
            name="predict",
            exist_ok=True
        )
        
        # Process results
        detected_classes = set()
        for result in results:
            for box in result.boxes:
                detected_classes.add(model.names[int(box.cls.item())])
        
        # Convert video format
        result_dir = os.path.join(RESULT_FOLDER, "predict")
        base_name = os.path.splitext(uploaded_file.name)[0]
        avi_path = max(glob.glob(os.path.join(result_dir, f"{base_name}*.avi")), key=os.path.getctime)
        mp4_path = avi_path.replace(".avi", ".mp4")
        
        if convert_video_to_mp4(avi_path, mp4_path):
            return mp4_path, detected_classes
        return None, None
        
    except Exception as e:
        st.error(f"Video prediction failed: {str(e)}")
        return None, None

# ---------------------- UI Components ----------------------
def sidebar():
    with st.sidebar:
        st.title("🖼️ ISL Detection System")
        app_mode = st.radio("Select Mode", ["📷 Image Detection", "🎥 Video Analysis", "📸 Live Capture"])
        st.markdown("---")
        with st.expander("ℹ️ Instructions"):
            st.markdown("""1. Select mode\n2. Upload media\n3. Detect objects""")
        return app_mode

# ---------------------- Main Application ----------------------
def main():
    # Custom CSS
    st.markdown("""
        <style>
        .main { background: #f8f9fa; }
        .stButton>button { background: #4a90e2; color: white; border-radius: 8px; }
        .result-box { border: 2px solid #e0e0e0; border-radius: 10px; padding: 1rem; }
        </style>
        """, unsafe_allow_html=True)
    
    app_mode = sidebar()
    st.title("ISL - YOLO Object Detection")
    
    if "Image" in app_mode:
        uploaded_file = st.file_uploader("Upload image", type=ALLOWED_IMAGE_TYPES)
        if uploaded_file and st.button("🔍 Detect Objects"):
            with st.spinner("Analyzing..."):
                result_path = predict_image(uploaded_file)
                if result_path:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.image(uploaded_file, use_container_width=True, caption="Original Image")
                    with col2:
                        st.image(result_path, use_container_width=True, caption="Detection Result")
                        success_animation()
    
    elif "Video" in app_mode:
        uploaded_file = st.file_uploader("Upload video", type=ALLOWED_VIDEO_TYPES)
        if uploaded_file and st.button("🔍 Analyze Video"):
            with st.spinner("Processing..."):
                result_path, classes = predict_video(uploaded_file)
                if result_path:
                    st.video(result_path)
                    if classes:
                        st.subheader("Detected Classes")
                        st.write(", ".join(classes))
    
    else:  # Live Camera
        frame = st.camera_input("Take a picture")
        if frame and st.button("🔍 Detect"):
            with st.spinner("Processing..."):
                result_path = predict_image(frame)
                if result_path:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.image(frame, use_container_width=True, caption="Original Capture")
                    with col2:
                        st.image(result_path, use_container_width=True, caption="Detection Result")
    
    # Footer
    st.markdown("---")
    st.markdown("🚀 Powered by Diya Group | 🔐 Secure Processing", unsafe_allow_html=True)

if __name__ == "__main__":
    main()