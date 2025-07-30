from flask import Flask, jsonify, render_template, Response
from gps_reader import get_latest_gps
from AI import YOLOBallController

app = Flask(__name__)
ball_detector = YOLOBallController()

# PERBAIKAN: Buat list untuk menyimpan riwayat geo_tags
geo_tag_history = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    gps_entry = get_latest_gps()

    # Tambahkan entri baru ke riwayat jika ada
    if gps_entry:
        geo_tag_history.append(gps_entry)
        # Batasi agar tidak terlalu banyak, misal 100 entri terakhir
        if len(geo_tag_history) > 100:
            geo_tag_history.pop(0)

    result = {
        # ... (bagian lain dari JSON)
        "attitude_info": {
            "sog": gps_entry["sog"] if gps_entry else 0,
            "cog": gps_entry["cog"] if gps_entry else 0,
            # Mengirimkan riwayat lintasan untuk grafik
            "trajectory": [[entry["longitude"], entry["latitude"]] for entry in geo_tag_history]
        },
        # PERBAIKAN: Kirim seluruh riwayat untuk tabel
        "geo_tags": geo_tag_history,
        # ... (bagian lain dari JSON)
    }

    return jsonify(result)

@app.route('/video_feed')
def video_feed():
       return Response(ball_detector.generate_frames(),
                   mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True, port=5050)
