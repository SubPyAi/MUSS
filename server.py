import cv2
import mss
import numpy as np
from flask import Flask, render_template, Response, request, jsonify # type: ignore

with open("server.cfg", "r") as f:
    config = f.read().split("\n")
    for i in range(0, len(config)):
        config[i] = config[i].split("=")[1]
    print(config)
    SERVER_IP = config[0]
    SERVER_PORT = int(config[1])

# Create a Flask app instance
app = Flask(__name__, static_url_path='/static')

# Set to keep track of RTCPeerConnection instances
pcs = set()

# Function to capture screen frames using mss
def generate_screen_frames():
    sct = mss.mss()
    monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}  # Adjust to your screen resolution

    while True:
        img = sct.grab(monitor)
        frame = cv2.cvtColor(np.array(img), cv2.COLOR_BGRA2BGR)

        # Encode frame as JPEG (optional)
        ret, buffer = cv2.imencode('.jpg', frame)
        if ret:
            frame = buffer.tobytes()

            # Concatenate frame and yield for streaming
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# (Rest of your code remains the same)

# Route to stream video frames
@app.route('/')
def video_feed():
    return Response(generate_screen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True, host=SERVER_IP, port=SERVER_PORT)