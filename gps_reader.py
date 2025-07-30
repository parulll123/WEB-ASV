import serial
import pynmea2
from datetime import datetime

def get_latest_gps():
    try:
        with serial.Serial('/dev/ttyUSB0', baudrate=9600, timeout=1) as ser:
            while True:
                line = ser.readline().decode('utf-8', errors='ignore')
                if line.startswith('$GPRMC'):
                    msg = pynmea2.parse(line)
                    if msg.status == 'A':  # Valid GPS fix
                        gps_date = msg.datestamp.strftime('%Y-%m-%d') if msg.datestamp else "N/A"
                        gps_time = msg.timestamp.strftime('%H:%M:%S') if msg.timestamp else "N/A"
                        return {
                            "timestamp": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),  # optional: sistem UTC
                            "gps_date": gps_date,     # dari satelit
                            "gps_time": gps_time,     # dari satelit
                            "latitude": msg.latitude,
                            "longitude": msg.longitude,
                            "sog": float(msg.spd_over_grnd) * 1.852,  # knots to km/h
                            "cog": float(msg.true_course)
                        }
    except Exception as e:
        print(f"[GPS ERROR] {e}")
        return {
            "timestamp": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            "gps_date": "N/A",
            "gps_time": "N/A",
            "latitude": 0.0,
            "longitude": 12.0,
            "sog": 0.0,
            "cog": 0.0
        }
