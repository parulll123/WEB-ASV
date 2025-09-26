# app.py

from flask import Flask, jsonify, render_template
from flask_mqtt import Mqtt
import json

app = Flask(__name__)

# --- KONFIGURASI KONEKSI MQTT ---
# Ganti dengan alamat broker MQTT Anda.
# Anda bisa menggunakan broker publik seperti 'broker.hivemq.com' untuk testing.
app.config['MQTT_BROKER_URL'] = '10.61.60.238'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''  # Kosongkan jika tidak ada autentikasi
app.config['MQTT_PASSWORD'] = ''  # Kosongkan jika tidak ada autentikasi
app.config['MQTT_KEEPALIVE'] = 5  # Detik
app.config['MQTT_TLS_ENABLED'] = False

mqtt = Mqtt(app)

# --- VARIABEL GLOBAL UNTUK MENYIMPAN DATA TERAKHIR ---
# Inisialisasi dengan struktur data default agar tidak error saat pertama kali dimuat
latest_data = {
    "attitude_info": {
        "sog": 0,
        "speed" : 0,
        "cog": 0,
        "trajectory": []
    },
    "geo_tags": [],
    "floating_ball_checklist": [],
    "other_indicators": {
        "battery_level": 0
    }
}
trajectory_history = []

# --- FUNGSI CALLBACK MQTT ---

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    """
    Fungsi ini dipanggil saat aplikasi berhasil terhubung ke broker MQTT.
    Langsung subscribe ke topik yang dibutuhkan.
    """
    if rc == 0:
        print("Connected to MQTT Broker!")
        mqtt.subscribe('boat/geotag')
        mqtt.subscribe('boat/checklist')
    else:
        print(f"Failed to connect, return code {rc}\n")


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    """
    Fungsi ini dipanggil setiap kali ada pesan masuk dari topik yang di-subscribe.
    """
    global latest_data, trajectory_history
    
    topic = message.topic
    payload = json.loads(message.payload.decode())
    
    print(f"Received message on topic {topic}: {payload}")

    if topic == 'boat/geotag':
        # Update data geo-tag dan lintasan
        new_lat = payload.get("latitude", 0)
        new_lon = payload.get("longitude", 0)
        latest_data["attitude_info"]["speed"] = payload.get("speed", 0)
        latest_data["attitude_info"]["sog"] = payload.get("sog", 0)
        latest_data["attitude_info"]["cog"] = payload.get("cog", 0)
        latest_data["geo_tags"] = [payload] # Hanya tampilkan data terakhir di tabel
        latest_data["other_indicators"]["battery_level"] = payload.get("battery", 0)

        # Tambahkan titik baru ke riwayat lintasan
        trajectory_history.append([new_lat, new_lon])
        
        # Batasi panjang riwayat (opsional)
        if len(trajectory_history) > 200:
            trajectory_history.pop(0)
            
        latest_data["attitude_info"]["trajectory"] = trajectory_history

    elif topic == 'boat/checklist':
        # Update data checklist bola
        latest_data["floating_ball_checklist"] = payload.get("balls", [])

# --- RUTE FLASK ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    """
    Endpoint ini sekarang hanya berfungsi untuk mengirimkan data terakhir
    yang disimpan di variabel global 'latest_data'.
    """
    return jsonify(latest_data)

if __name__ == '__main__':
    app.run(debug=True, port=5050)