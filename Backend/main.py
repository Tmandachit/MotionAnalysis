from flask import Flask, request, jsonify
from flask_cors import CORS
import os

from backend_modules.video_utils import load_video
from backend_modules.pose_detector import extract_poses
from backend_modules.analysis import analyze_swing

app = Flask(__name__)
CORS(app)

@app.route("/analyze", methods=["POST"])
def analyze():
    file = request.files.get("video")
    if not file:
        return jsonify({"error": "No video uploaded"}), 400

    filepath = os.path.join("../data", file.filename)
    file.save(filepath)

    frames = load_video(filepath)
    keypoints = extract_poses(frames)
    results = analyze_swing(keypoints)

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
