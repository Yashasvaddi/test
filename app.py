from flask import Flask, render_template, Response, request,send_from_directory
import cv2
import os

app = Flask(__name__)

# Initialize camera
camera = cv2.VideoCapture(0)

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # Example backend processing: convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray=cv2.flip(gray,1)
            # Convert back to color (to maintain 3 channels for JPEG encoding)
            processed = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

            # Encode as JPEG
            ret, buffer = cv2.imencode('.jpg', processed)
            frame = buffer.tobytes()

            # Yield frame to frontend
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    port=int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0",port=port,debug=True)
