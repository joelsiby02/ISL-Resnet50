# import streamlit as st
# import requests
# import os
# from PIL import Image

# API_URL = "http://127.0.0.1:5000/predict"  # Change this if running Flask on a different host

# st.title("YOLO Object Detection")

# uploaded_file = st.file_uploader("Choose an image...")
# if uploaded_file is not None:
#     # Save uploaded image
#     image_path = os.path.join("temp", uploaded_file.name)
#     os.makedirs("temp", exist_ok=True)
#     with open(image_path, "wb") as f:
#         f.write(uploaded_file.getbuffer())
    
#     st.image(image_path, caption="Uploaded Image", use_container_width=True)
    
#     if st.button("Run Detection"):
#         files = {"file": open(image_path, "rb")}
#         response = requests.post(API_URL, files=files)
        
#         if response.status_code == 200:
#             result_image_path = response.json().get("result_image")
#             if result_image_path:
#                 result_url = f"http://127.0.0.1:5000/results/{os.path.basename(result_image_path)}"
#                 st.image(result_url, caption="Detected Objects", use_container_width=True)
#             else:
#                 st.error("Error: No result image found.")
#         else:
#             st.error("Error: Unable to process the image.")







# import streamlit as st
# import requests
# import os
# import atexit

# # Configuration
# API_URL = "http://127.0.0.1:5000/predict"
# ALLOWED_IMAGE_TYPES = ["jpg", "jpeg", "png"]
# ALLOWED_VIDEO_TYPES = ["mp4", "avi", "mov"]

# # Cleanup function
# def cleanup():
#     if os.path.exists("temp"):
#         for f in os.listdir("temp"):
#             os.remove(os.path.join("temp", f))
# atexit.register(cleanup)

# # UI Configuration
# st.set_page_config(
#     page_title="YOLO Object Detection",
#     page_icon="🔍",
#     layout="wide"
# )

# # Sidebar Navigation
# st.sidebar.title("Navigation")
# app_mode = st.sidebar.radio("Select Detection Mode", 
#     ["Image Detection", "Video Detection", "Live Camera"])

# st.sidebar.markdown("---")
# st.sidebar.info(
#     """
#     ### Instructions
#     1. Select detection mode
#     2. Upload file or use camera
#     3. Click detection button
#     """
# )

# # Main Content Area
# st.title("YOLO Object Detection System")
# st.markdown("---")

# def image_detection():
#     st.header("📷 Image Detection")
#     with st.expander("Upload Image", expanded=True):
#         uploaded_file = st.file_uploader(
#             "Choose an image...", 
#             type=ALLOWED_IMAGE_TYPES,
#             key="image_upload"
#         )
        
#     if uploaded_file is not None:
#         col1, col2 = st.columns(2)
#         with col1:
#             st.subheader("Input Image")
#             image_path = os.path.join("temp", uploaded_file.name)
#             os.makedirs("temp", exist_ok=True)
#             with open(image_path, "wb") as f:
#                 f.write(uploaded_file.getbuffer())
#             st.image(image_path, use_container_width=True)
        
#         if st.button("🔍 Run Image Detection"):
#             with st.spinner("Detecting objects..."):
#                 try:
#                     files = {"file": open(image_path, "rb")}
#                     response = requests.post(API_URL, files=files)
                    
#                     if response.status_code == 200:
#                         result_image_path = response.json().get("result_image")
#                         if result_image_path:
#                             result_url = f"http://127.0.0.1:5000{result_image_path}"
#                             with col2:
#                                 st.subheader("Detection Results")
#                                 st.image(result_url, use_container_width=True)
#                                 st.success("Detection completed successfully!")
#                         else:
#                             st.error("No result image found in response")
#                     else:
#                         st.error(f"API Error: {response.text}")
#                 except Exception as e:
#                     st.error(f"Detection failed: {str(e)}")

# def video_detection():
#     st.header("🎥 Video Detection")
#     with st.expander("Upload Video", expanded=True):
#         uploaded_video = st.file_uploader(
#             "Choose a video...", 
#             type=ALLOWED_VIDEO_TYPES,
#             key="video_upload"
#         )
    
#     if uploaded_video is not None:
#         col1, col2 = st.columns(2)
#         with col1:
#             st.subheader("Input Video")
#             video_path = os.path.join("temp", uploaded_video.name)
#             os.makedirs("temp", exist_ok=True)
#             with open(video_path, "wb") as f:
#                 f.write(uploaded_video.getbuffer())
#             st.video(video_path)
        
#         if st.button("🔍 Run Video Detection"):
#             with st.spinner("Processing video..."):
#                 try:
#                     files = {"file": open(video_path, "rb")}
#                     response = requests.post("http://127.0.0.1:5000/predict_video", files=files)
                    
#                     if response.status_code == 200:
#                         result = response.json()
#                         result_video = result.get("result_video")
#                         detected_classes = result.get("detected_classes", [])
                        
#                         if result_video:
#                             result_url = f"http://127.0.0.1:5000{result_video}"
#                             with col2:
#                                 st.subheader("Processed Video")
#                                 st.video(result_url, format="video/mp4")
#                                 st.success("Video processing completed!")
#                                 st.markdown("**Detected Classes:**")
#                                 for cls in detected_classes:
#                                     st.markdown(f"- {cls}")
#                         else:
#                             st.error("No result video found in response")
#                     else:
#                         st.error(f"API Error: {response.text}")
#                 except Exception as e:
#                     st.error(f"Video processing failed: {str(e)}")

# def live_camera():
#     st.header("📸 Live Camera Inference")
#     with st.expander("Camera Controls", expanded=True):
#         frame = st.camera_input("Capture real-time frame")
    
#     if frame:
#         col1, col2 = st.columns(2)
#         with col1:
#             st.subheader("Captured Frame")
#             frame_path = os.path.join("temp", frame.name)
#             os.makedirs("temp", exist_ok=True)
#             with open(frame_path, "wb") as f:
#                 f.write(frame.getbuffer())
#             st.image(frame_path, use_container_width=True)
        
#         with st.spinner("Processing frame..."):
#             try:
#                 files = {"file": open(frame_path, "rb")}
#                 response = requests.post("http://127.0.0.1:5000/predict_frame", files=files)
                
#                 if response.status_code == 200:
#                     result_image = response.json().get("result_image")
#                     detected_classes = response.json().get("detected_classes", [])
#                     if result_image:
#                         result_url = f"http://127.0.0.1:5000{result_image}"
#                         with col2:
#                             st.subheader("Processed Frame")
#                             st.image(result_url, use_container_width=True)
#                             st.success("Frame processed successfully!")
#                             st.markdown("**Detected Classes:**")
#                             for cls in detected_classes:
#                                 st.markdown(f"- {cls}")
#                     else:
#                         st.error("No result image found in response")
#                 else:
#                     st.error(f"API Error: {response.text}")
#             except Exception as e:
#                 st.error(f"Frame processing failed: {str(e)}")

# # Route to appropriate function
# if app_mode == "Image Detection":
#     image_detection()
# elif app_mode == "Video Detection":
#     video_detection()
# elif app_mode == "Live Camera":
#     live_camera()

# # Add some custom styling
# st.markdown("""
#     <style>
#     .reportview-container {
#         background: #f0f2f6
#     }
#     .sidebar .sidebar-content {
#         background: #ffffff
#     }
#     div[data-testid="stExpander"] details {
#         background: #ffffff;
#         border-radius: 8px;
#         box-shadow: 0 2px 4px rgba(0,0,0,0.1);
#     }
#     </style>
#     """, unsafe_allow_html=True)



# import streamlit as st
# import requests
# import os
# import atexit
# import shutil
# from streamlit_image_comparison import image_comparison
# from streamlit_extras.let_it_rain import rain

# # Configuration
# API_URL = "http://127.0.0.1:5000/predict"
# ALLOWED_IMAGE_TYPES = ["jpg", "jpeg", "png"]
# ALLOWED_VIDEO_TYPES = ["mp4", "avi", "mov"]

# # Improved cleanup function with retry mechanism
# def cleanup():
#     if os.path.exists("temp"):
#         for _ in range(3):  # Retry up to 3 times
#             try:
#                 shutil.rmtree("temp")
#                 break
#             except Exception as e:
#                 if _ == 2:  # Final attempt
#                     st.error(f"Cleanup failed: {str(e)}")
# atexit.register(cleanup)

# # UI Configuration
# st.set_page_config(
#     page_title="VisionAI Detector",
#     page_icon="🖼️",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # Custom CSS
# st.markdown("""
#     <style>
#     .main {
#         background: #f8f9fa;
#     }
#     .stButton>button {
#         background: #4a90e2;
#         color: white;
#         border-radius: 8px;
#         padding: 0.5rem 1.5rem;
#         transition: all 0.3s;
#     }
#     .stButton>button:hover {
#         background: #357abd;
#         transform: scale(1.05);
#     }
#     .card {
#         background: white;
#         border-radius: 12px;
#         padding: 1.5rem;
#         box-shadow: 0 4px 6px rgba(0,0,0,0.1);
#         margin-bottom: 1.5rem;
#     }
#     </style>
#     """, unsafe_allow_html=True)

# # Sidebar Navigation
# with st.sidebar:
#     st.title("🖼️ ISL Detection System")
#     st.markdown("---")
#     app_mode = st.radio("Select Mode", 
#         ["📷 Image Detection", "🎥 Video Analysis", "📸 Live Capture"])
    
#     st.markdown("---")
#     with st.expander("ℹ️ Instructions", expanded=True):
#         st.markdown("""
#         **How to Use:**
#         1. Select detection mode
#         2. Upload media or use camera
#         3. Click detection button
#         4. View results side-by-side
        
#         **Supported Formats:**
#         - Images: JPG, PNG, JPEG
#         - Videos: MP4, AVI, MOV
#         """)

# # Main Content
# st.title("ISL - Resnet 50 / YOLO V11 ")
# st.markdown("---")

# def success_animation():
#     rain(emoji="🎉", font_size=20, falling_speed=3, animation_length=1)

# def safe_file_operation(file_path, content, mode='wb'):
#     os.makedirs(os.path.dirname(file_path), exist_ok=True)
#     with open(file_path, mode) as f:
#         f.write(content)

# def image_detection():
#     with st.container():
#         col1, col2 = st.columns([1, 1], gap="large")
        
#         with col1:
#             with st.form("image-upload"):
#                 st.subheader("Upload Image")
#                 uploaded_file = st.file_uploader(
#                     "Drag & drop or select file",
#                     type=ALLOWED_IMAGE_TYPES,
#                     label_visibility="collapsed"
#                 )
#                 submitted = st.form_submit_button("Upload & Process")
        
#         if uploaded_file and submitted:
#             with col1:
#                 with st.spinner("Processing image..."):
#                     try:
#                         image_path = os.path.join("temp", uploaded_file.name)
#                         safe_file_operation(image_path, uploaded_file.getbuffer())
                        
#                         with open(image_path, "rb") as file:
#                             response = requests.post(API_URL, files={"file": file})
                        
#                         if response.status_code == 200:
#                             result_image_path = response.json().get("result_image")
#                             if result_image_path:
#                                 result_url = f"http://127.0.0.1:5000{result_image_path}"
#                                 with col2:
#                                     st.subheader("Detection Results")
#                                     image_comparison(
#                                         img1=image_path,
#                                         img2=result_url,
#                                         label1="Original",
#                                         label2="Processed",
#                                         width=700,
#                                         show_labels=True
#                                     )
#                                     success_animation()
#                                 try:
#                                     os.remove(image_path)
#                                 except Exception as e:
#                                     st.error(f"Cleanup error: {str(e)}")
#                             else:
#                                 st.error("Processing failed - no result image")
#                         else:
#                             st.error(f"API Error: {response.text}")
#                     except Exception as e:
#                         st.error(f"Error: {str(e)}")

# def video_detection():
#     with st.container():
#         col1, col2 = st.columns([1, 1], gap="large")
        
#         with col1:
#             with st.form("video-upload"):
#                 st.subheader("Upload Video")
#                 uploaded_video = st.file_uploader(
#                     "Drag & drop or select file",
#                     type=ALLOWED_VIDEO_TYPES,
#                     label_visibility="collapsed"
#                 )
#                 submitted = st.form_submit_button("Upload & Process")
        
#         if uploaded_video and submitted:
#             with col1:
#                 with st.spinner("Analyzing video..."):
#                     try:
#                         video_path = os.path.join("temp", uploaded_video.name)
#                         safe_file_operation(video_path, uploaded_video.getbuffer())
                        
#                         with open(video_path, "rb") as file:
#                             response = requests.post("http://127.0.0.1:5000/predict_video", files={"file": file})
                        
#                         if response.status_code == 200:
#                             result = response.json()
#                             result_video = result.get("result_video")
#                             detected_classes = result.get("detected_classes", [])
                            
#                             if result_video:
#                                 result_url = f"http://127.0.0.1:5000{result_video}"
#                                 with col2:
#                                     st.subheader("Analysis Results")
#                                     st.video(result_url)
#                                     st.success("Video processing completed!")
#                                     st.markdown("**Detected Objects:**")
#                                     cols = st.columns(3)
#                                     for idx, cls in enumerate(detected_classes):
#                                         cols[idx%3].markdown(f"🔹 {cls.capitalize()}")
#                                     success_animation()
#                                 try:
#                                     os.remove(video_path)
#                                 except Exception as e:
#                                     st.error(f"Cleanup error: {str(e)}")
#                             else:
#                                 st.error("Processing failed - no result video")
#                         else:
#                             st.error(f"API Error: {response.text}")
#                     except Exception as e:
#                         st.error(f"Error: {str(e)}")

# def live_camera():
#     with st.container():
#         col1, col2 = st.columns([1, 1], gap="large")
        
#         with col1:
#             st.subheader("Real-time Detection")
#             frame = st.camera_input("Look here 👇", label_visibility="collapsed")
            
#             if frame:
#                 with st.spinner("Processing frame..."):
#                     try:
#                         frame_path = os.path.join("temp", frame.name)
#                         safe_file_operation(frame_path, frame.getbuffer())
                        
#                         with open(frame_path, "rb") as file:
#                             response = requests.post("http://127.0.0.1:5000/predict_frame", files={"file": file})
                        
#                         if response.status_code == 200:
#                             result_image = response.json().get("result_image")
#                             detected_classes = response.json().get("detected_classes", [])
#                             if result_image:
#                                 result_url = f"http://127.0.0.1:5000{result_image}"
#                                 with col2:
#                                     st.subheader("Detection Results")
#                                     image_comparison(
#                                         img1=frame_path,
#                                         img2=result_url,
#                                         label1="Original",
#                                         label2="Processed",
#                                         width=700,
#                                         show_labels=True
#                                     )
#                                     st.markdown("**Identified Objects:**")
#                                     for cls in detected_classes:
#                                         st.markdown(f"✅ {cls.capitalize()}")
#                                     success_animation()
#                                 try:
#                                     os.remove(frame_path)
#                                 except Exception as e:
#                                     st.error(f"Cleanup error: {str(e)}")
#                             else:
#                                 st.error("Processing failed - no result image")
#                         else:
#                             st.error(f"API Error: {response.text}")
#                     except Exception as e:
#                         st.error(f"Error: {str(e)}")

# # Routing
# if "📷 Image Detection" in app_mode:
#     image_detection()
# elif "🎥 Video Analysis" in app_mode:
#     video_detection()
# elif "📸 Live Capture" in app_mode:
#     live_camera()

# # Footer
# st.markdown("---")
# st.markdown("""
# <div style="text-align: center; color: #666; padding: 1rem;">
#     🚀 Powered by Diya Group | 🔐 Secure Processing | 📧 support@akash.com
# </div>
# """, unsafe_allow_html=True)



import streamlit as st
import requests
import os
import atexit
import shutil
from streamlit_extras.let_it_rain import rain

# Configuration
API_URL = "http://127.0.0.1:5000/predict"
ALLOWED_IMAGE_TYPES = ["jpg", "jpeg", "png"]
ALLOWED_VIDEO_TYPES = ["mp4", "avi", "mov"]

# Improved cleanup function
def cleanup():
    if os.path.exists("temp"):
        try:
            shutil.rmtree("temp")
        except Exception as e:
            st.error(f"Cleanup error: {str(e)}")
atexit.register(cleanup)

# UI Configuration
st.set_page_config(
    page_title="VisionAI Detector",
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        background: #f8f9fa;
    }
    .stButton>button {
        background: #4a90e2;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background: #357abd;
        transform: scale(1.05);
    }
    .result-box {
        border: 2px solid #e0e0e0;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar Navigation
with st.sidebar:
    st.title("🖼️ ISL Detection System")
    st.markdown("---")
    app_mode = st.radio("Select Mode", 
        ["📷 Image Detection", "🎥 Video Analysis", "📸 Live Capture"])
    
    st.markdown("---")
    with st.expander("ℹ️ Instructions", expanded=True):
        st.markdown("""
        **How to Use:**
        1. Select detection mode
        2. Upload media or use camera
        3. Click detection button
        4. View results below
        
        **Supported Formats:**
        - Images: JPG, PNG, JPEG
        - Videos: MP4, AVI, MOV
        """)

# Main Content
st.title("ISL - Resnet 50 / YOLO V11 ")
st.markdown("---")

def success_animation():
    rain(emoji="🎉", font_size=20, falling_speed=3, animation_length=1)

def safe_file_operation(file_path, content):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(content)

def image_detection():
    with st.container():
        st.subheader("Image Detection")
        uploaded_file = st.file_uploader(
            "Upload an image",
            type=ALLOWED_IMAGE_TYPES,
            label_visibility="collapsed"
        )
        
        if uploaded_file:
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Original Image")
                image_path = os.path.join("temp", uploaded_file.name)
                safe_file_operation(image_path, uploaded_file.getbuffer())
                st.image(image_path, use_container_width=True)
            
            if st.button("🔍 Detect Objects", use_container_width=True):
                with st.spinner("Analyzing image..."):
                    try:
                        with open(image_path, "rb") as file:
                            response = requests.post(API_URL, files={"file": file})
                        
                        if response.status_code == 200:
                            result = response.json()
                            result_url = f"http://127.0.0.1:5000{result.get('result_image', '')}"
                            
                            with col2:
                                st.subheader("Detection Results")
                                with st.container(border=True):
                                    st.image(result_url, use_container_width=True)
                                    detected_classes = result.get("detected_classes", [])
                                    if detected_classes:
                                        st.markdown("**Detected Objects:**")
                                        for cls in detected_classes:
                                            st.markdown(f"- {cls.capitalize()}")
                                    success_animation()
                            
                            # Cleanup temp file after successful processing
                            try:
                                os.remove(image_path)
                            except Exception as e:
                                st.error(f"Cleanup warning: {str(e)}")
                                
                        else:
                            st.error(f"API Error: {response.text}")
                    except Exception as e:
                        st.error(f"Processing Error: {str(e)}")

def video_detection():
    with st.container():
        st.subheader("Video Analysis")
        uploaded_video = st.file_uploader(
            "Upload a video",
            type=ALLOWED_VIDEO_TYPES,
            label_visibility="collapsed"
        )
        
        if uploaded_video:
            video_path = os.path.join("temp", uploaded_video.name)
            safe_file_operation(video_path, uploaded_video.getbuffer())
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Original Video")
                st.video(video_path)
            
            if st.button("🔍 Analyze Video", use_container_width=True):
                with st.spinner("Processing video..."):
                    try:
                        with open(video_path, "rb") as file:
                            response = requests.post("http://127.0.0.1:5000/predict_video", files={"file": file})
                        
                        if response.status_code == 200:
                            result = response.json()
                            result_url = f"http://127.0.0.1:5000{result.get('result_video', '')}"
                            
                            with col2:
                                st.subheader("Analysis Results")
                                with st.container(border=True):
                                    st.video(result_url)
                                    detected_classes = result.get("detected_classes", [])
                                    if detected_classes:
                                        st.markdown("**Detected Objects:**")
                                        cols = st.columns(2)
                                        for idx, cls in enumerate(detected_classes):
                                            cols[idx%2].markdown(f"- {cls.capitalize()}")
                                    success_animation()
                            
                            try:
                                os.remove(video_path)
                            except Exception as e:
                                st.error(f"Cleanup warning: {str(e)}")
                                
                        else:
                            st.error(f"API Error: {response.text}")
                    except Exception as e:
                        st.error(f"Processing Error: {str(e)}")

def live_camera():
    with st.container():
        st.subheader("Real-time Detection")
        frame = st.camera_input("Capture a frame", label_visibility="collapsed")
        
        if frame:
            frame_path = os.path.join("temp", frame.name)
            safe_file_operation(frame_path, frame.getbuffer())
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Captured Frame")
                st.image(frame_path, use_container_width=True)
            
            with st.spinner("Processing frame..."):
                try:
                    with open(frame_path, "rb") as file:
                        response = requests.post("http://127.0.0.1:5000/predict_frame", files={"file": file})
                    
                    if response.status_code == 200:
                        result = response.json()
                        result_url = f"http://127.0.0.1:5000{result.get('result_image', '')}"
                        
                        with col2:
                            st.subheader("Detection Results")
                            with st.container(border=True):
                                st.image(result_url, use_container_width=True)
                                detected_classes = result.get("detected_classes", [])
                                if detected_classes:
                                    st.markdown("**Detected Objects:**")
                                    for cls in detected_classes:
                                        st.markdown(f"- {cls.capitalize()}")
                                success_animation()
                        
                        try:
                            os.remove(frame_path)
                        except Exception as e:
                            st.error(f"Cleanup warning: {str(e)}")
                            
                    else:
                        st.error(f"API Error: {response.text}")
                except Exception as e:
                    st.error(f"Processing Error: {str(e)}")

# Routing
if "📷 Image Detection" in app_mode:
    image_detection()
elif "🎥 Video Analysis" in app_mode:
    video_detection()
elif "📸 Live Capture" in app_mode:
    live_camera()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    🚀 Powered by Diya Group | 🔐 Secure Processing | 📧 support@akash.com
</div>
""", unsafe_allow_html=True)