# from flask import Flask, request, jsonify, send_from_directory
# from ultralytics import YOLO
# import os
# from PIL import Image

# app = Flask(__name__)
# UPLOAD_FOLDER = "uploads"
# RESULT_FOLDER = "runs/detect/predict"
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# os.makedirs(RESULT_FOLDER, exist_ok=True)

# # Load YOLO model
# MODEL_PATH = "my_model.pt"  # Ensure this is the correct model path
# model = YOLO(MODEL_PATH)

# @app.route("/predict", methods=["POST"])
# def predict():
#     if "file" not in request.files:
#         return jsonify({"error": "No file uploaded"}), 400
    
#     file = request.files["file"]
#     image_path = os.path.join(UPLOAD_FOLDER, file.filename)
#     file.save(image_path)
    
#     # Run YOLO prediction (forcing it to always save in "runs/detect/predict/")
#     model.predict(source=image_path, save=True, project="runs/detect", name="predict", exist_ok=True)

#     # Construct the correct path to the predicted image
#     result_image_path = os.path.join("runs/detect/predict", file.filename)

#     # Ensure the predicted image exists before returning the response
#     if not os.path.exists(result_image_path):
#         return jsonify({"error": "Prediction failed, output image not found"}), 500

#     return jsonify({"message": "Prediction complete", "result_image": f"/results/{file.filename}"})


# @app.route("/results/<filename>")
# def get_result_image(filename):
#     return send_from_directory(RESULT_FOLDER, filename)

# if __name__ == "__main__":
#     app.run(debug=True)





from flask import Flask, request, jsonify, send_from_directory
from ultralytics import YOLO
import os
import glob
import cv2
import shutil

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
RESULT_FOLDER = "runs/detect/predict"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

MODEL_PATH = "my_model.pt"
model = YOLO(MODEL_PATH)

def convert_video_to_mp4(input_path, output_path):
    cap = None
    out = None
    try:
        cap = cv2.VideoCapture(input_path)
        if not cap.isOpened():
            raise ValueError(f"Could not open video file: {input_path}")
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        fourcc = cv2.VideoWriter_fourcc(*'avc1')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            out.write(frame)
        
    finally:
        if cap: cap.release()
        if out: out.release()
        try:
            os.remove(input_path)
        except Exception as e:
            app.logger.error(f"Error deleting temp file: {str(e)}")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400
        
        file = request.files["file"]
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        
        model.predict(source=file_path, save=True, project="runs/detect", name="predict", exist_ok=True)
        
        result_path = os.path.join(RESULT_FOLDER, file.filename)
        if not os.path.exists(result_path):
            return jsonify({"error": "Prediction failed"}), 500
        
        return jsonify({
            "message": "Prediction complete", 
            "result_image": f"/results/{file.filename}"
        })
    finally:
        try:
            os.remove(file_path)
        except Exception as e:
            app.logger.error(f"Error cleaning upload: {str(e)}")

@app.route("/predict_video", methods=["POST"])
def predict_video():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No video uploaded"}), 400
        
        file = request.files["file"]
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        
        detected_classes = set()
        results = model.predict(source=file_path, save=True, project="runs/detect", name="predict", exist_ok=True)
        
        for result in results:
            for box in result.boxes:
                cls_id = int(box.cls.item())
                detected_classes.add(model.names[cls_id])
        
        base_name = os.path.splitext(file.filename)[0]
        avi_files = glob.glob(os.path.join(RESULT_FOLDER, f"{base_name}*.avi"))
        if not avi_files:
            return jsonify({"error": "Output video not found"}), 500
        
        avi_path = max(avi_files, key=os.path.getctime)
        mp4_path = os.path.splitext(avi_path)[0] + ".mp4"
        
        try:
            convert_video_to_mp4(avi_path, mp4_path)
        except Exception as e:
            return jsonify({"error": f"Video conversion failed: {str(e)}"}), 500
        
        return jsonify({
            "result_video": f"/results/{os.path.basename(mp4_path)}",
            "detected_classes": list(detected_classes)
        })
    finally:
        try:
            os.remove(file_path)
        except Exception as e:
            app.logger.error(f"Error cleaning upload: {str(e)}")

@app.route("/predict_frame", methods=["POST"])
def predict_frame():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No frame uploaded"}), 400
        
        file = request.files["file"]
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        
        detected_classes = set()
        results = model.predict(source=file_path, save=True, project="runs/detect", name="predict", exist_ok=True)
        
        for result in results:
            for box in result.boxes:
                cls_id = int(box.cls.item())
                detected_classes.add(model.names[cls_id])
        
        result_path = os.path.join(RESULT_FOLDER, file.filename)
        if not os.path.exists(result_path):
            return jsonify({"error": "Prediction failed"}), 500
        
        return jsonify({
            "result_image": f"/results/{file.filename}",
            "detected_classes": list(detected_classes)
        })
    finally:
        try:
            os.remove(file_path)
        except Exception as e:
            app.logger.error(f"Error cleaning upload: {str(e)}")

@app.route("/results/<filename>")
def get_result_file(filename):
    mimetype = 'application/octet-stream'
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        mimetype = 'image/*'
    elif filename.lower().endswith('.mp4'):
        mimetype = 'video/mp4'
    
    return send_from_directory(RESULT_FOLDER, filename, mimetype=mimetype)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)