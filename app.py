from flask import Flask, jsonify, render_template
from gps_reader import get_latest_gps

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    gps_entry = get_latest_gps()

    result = {
        "position_log": {
            "preparation": True,
            "start": True,
            "floating_ball_set": 5,
            "mission_surface_imaging": True,
            "mission_underwater_imaging": True,
            "finish": False
        },
        "attitude_info": {
            "sog": gps_entry["sog"],
            "cog": gps_entry["cog"],
            "trajectory": [[gps_entry["longitude"], gps_entry["latitude"]]]
        },
        "geo_tags": [gps_entry],  # Bisa disesuaikan jika ingin simpan banyak
        "other_indicators": {
            "battery_level": 85,
            "visual_video_url": "https://www.youtube.com/embed/live_stream?channel=xxx"
        }
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5050)
