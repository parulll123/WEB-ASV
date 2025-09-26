import paho.mqtt.client as mqtt
import json

# Konfigurasi broker
broker = "public..com"
port = 1883
topic_geotag = "boat/geotag"
topic_checklist = "boat/checklist"

# Buat client
client = mqtt.Client()
client.connect(broker, port)

# Payload untuk boat/geotag
geotag_payload = {
    "latitude": -6.200123,
    "longitude": 106.811234,
    "sog": 5.25,
    "cog": 180.0,
    "battery": 75.0
}
client.publish(topic_geotag, json.dumps(geotag_payload))

# Payload untuk boat/checklist
checklist_payload = {
    "balls": [
        {"id": "Ball1", "checked": True},
        {"id": "Ball2", "checked": False},
        {"id": "Ball3", "checked": True}
    ]
}
client.publish(topic_checklist, json.dumps(checklist_payload))

# Putuskan koneksi
client.disconnect()