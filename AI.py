import cv2
from ultralytics import YOLO
import serial
import time

class YOLOBallController:
    def __init__(self):
        # Inisialisasi Serial
        try:
            self.arduino = serial.Serial('COM7', 9600, timeout=1)
            time.sleep(2)
            print("Koneksi Arduino berhasil.")
        except serial.SerialException as e:
            print(f"Gagal terhubung ke Arduino: {e}")
            self.arduino = None

        # Inisialisasi Model
        try:
            self.model = YOLO('best2.pt')
            print("Model YOLOv8 berhasil dimuat.")
        except Exception as e:
            print(f"Error saat load model: {e}")
            exit()

        # Inisialisasi Kamera
        self.cap = cv2.VideoCapture(0)
        self.frame_width = 640
        self.frame_height = 480
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.frame_width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.frame_height)

        self.setpoint = self.frame_width // 2
        self.last_command = ''

    def generate_frames(self):
        while True:
            success, frame = self.cap.read()
            if not success:
                break

            results = self.model(frame, stream=True, verbose=False)
            detected_balls = {}
            annotated_frame = frame.copy()

            for r in results:
                annotated_frame = r.plot()
                for box in r.boxes:
                    x1, y1, x2, y2 = box.xyxy[0]
                    conf = box.conf.item()
                    cls_id = int(box.cls.item())
                    class_name = self.model.names[cls_id]

                    if conf > 0.5:
                        center_x = int((x1 + x2) / 2)
                        center_y = int((y1 + y2) / 2)
                        detected_balls[class_name] = (center_x, center_y)

                        label = f"{class_name} {int(conf*100)}%"
                        cv2.putText(annotated_frame, label, (int(x1), int(y1) - 5),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

            # Kontrol logika
            if 'red-ball' in detected_balls and 'green-ball' in detected_balls:
                red_pos = detected_balls['red-ball']
                green_pos = detected_balls['green-ball']
                target_x = (red_pos[0] + green_pos[0]) // 2
                target_y = (red_pos[1] + green_pos[1]) // 2

                # Visualisasi
                cv2.circle(annotated_frame, (target_x, target_y), 7, (255, 0, 255), -1)
                cv2.line(annotated_frame, (self.setpoint, 0), (self.setpoint, self.frame_height), (0, 255, 0), 2)
                cv2.line(annotated_frame, (target_x, target_y), (self.setpoint, target_y), (255, 255, 0), 2)

                if abs(target_x - self.setpoint) < 25:
                    command = 'F'
                elif target_x < self.setpoint:
                    command = 'L'
                else:
                    command = 'R'
            else:
                command = 'S'

            if command != self.last_command:
                if self.arduino:
                    self.arduino.write(command.encode() + b'\n')
                self.last_command = command
                print(f"Command: {command} | Target X: {target_x if 'target_x' in locals() else '-'}")

            # Encode dan stream frame
            ret, buffer = cv2.imencode('.jpg', annotated_frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    def __del__(self):
        self.cap.release()
        if self.arduino:
            self.arduino.write(b'S\n')
            self.arduino.close()
        cv2.destroyAllWindows()
