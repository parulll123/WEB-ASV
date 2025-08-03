from flask import Flask, jsonify, render_template, Response
import cv2
import random
import time

# (kode Flask, VideoCapture, dan generate_frames() Anda yang lain tetap sama)
app = Flask(__name__)
camera = cv2.VideoCapture(0)

# --- SIMPAN RIWAYAT LINTASAN DI SINI ---
# Variabel global untuk menyimpan semua titik koordinat yang telah dilalui
trajectory_history = []

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/data')
def data():
    # Simulasi mendapatkan data GPS baru
    last_lat = trajectory_history[-1][0] if trajectory_history else -6.21
    last_lon = trajectory_history[-1][1] if trajectory_history else 106.89
    
    new_entry = {
        "latitude": last_lat + random.uniform(-0.0001, 0.0001),
        "longitude": last_lon + random.uniform(-0.0001, 0.0001),
        "sog": 20.1 + random.uniform(-0.5, 0.5),
        "cog": 45.5 + random.uniform(-1, 1),
        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
    }

    # --- TAMBAHKAN TITIK BARU KE RIWAYAT ---
    trajectory_history.append([new_entry["latitude"], new_entry["longitude"]])
    
    # Batasi riwayat agar tidak terlalu panjang (opsional)
    if len(trajectory_history) > 200:
        trajectory_history.pop(0)

    result = {
        "position_log": {
            "preparation": True, "start": True, "floating_ball_set": 5,
            "mission_surface_imaging": True, "mission_underwater_imaging": True, "finish": False
        },
        "attitude_info": {
            "sog": new_entry["sog"],
            "cog": new_entry["cog"],
            # --- KIRIM SELURUH RIWAYAT LINTASAN ---
            "trajectory": trajectory_history 
        },
        "geo_tags": [new_entry],
        "other_indicators": {
            "battery_level": 85,
            "visual_video_url": "https://www.youtube.com/embed/live_stream?channel=xxx"
        }
    }
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5050)