import serial
import pynmea2
import time
from datetime import datetime
 # Coba koneksi ke port serial
    # Catatan: '/dev/ttyUSB0' adalah untuk Linux. Di Windows biasanya 'COM3', 'COM4', dll.
def get_latest_gps():
    try:
        with serial.Serial('/dev/ttyUSB0', baudrate=9600, timeout=1) as ser:
            while True:
                line = ser.readline().decode('utf-8', errors='ignore')
                if line.startswith('$GPRMC'):
                    msg = pynmea2.parse(line)
                    if msg.status == 'A':  # Valid GPS fix
                        return {
                            "timestamp": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
                            "latitude": msg.latitude,
                            "longitude": msg.longitude,
                            "sog": float(msg.spd_over_grnd) * 1.852,  # Convert knots to km/h
                            "cog": float(msg.true_course)
                        }
    except Exception as e:
        print(f"[GPS ERROR] {e}")
        return {
            "timestamp": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            "latitude": 0.0,
            "longitude": 12.0,
            "sog": 0.0,
            "cog": 0.0
        }
