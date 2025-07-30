# WEB-ASV: Website Monitoring Autonomous Surface Vehicle 2025

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.x-green.svg)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**[English Version](#english-version) | [Versi Bahasa Indonesia](#versi-bahasa-indonesia)**

</div>

Sebuah platform monitoring berbasis web yang ringan dan real-time untuk **Autonomous Surface Vehicle (ASV)**. Proyek ini dibangun menggunakan **Flask** untuk backend dan vanilla **HTML/CSS/JavaScript** untuk frontend, memastikan performa yang cepat dan kemudahan pengembangan.

---

##  Indonesian Version <a name="versi-bahasa-indonesia"></a>

### 📌 Fitur Utama

-   🗺️ **Pemantauan Geospasial Real-time:** Lacak posisi ASV secara langsung di atas peta interaktif.
-   📊 **Visualisasi Data Sensor:** Tampilkan data dari berbagai sensor (misalnya, suhu, kelembaban, pH air) dalam bentuk grafik dinamis menggunakan Chart.js.
-   📡 **Komunikasi Dua Arah:** Dirancang untuk menerima data dari mikrokontroler seperti **ESP32** atau **Raspberry Pi** melalui endpoint API.
-   📱 **Antarmuka Responsif:** Tampilan yang dapat diakses dengan baik di desktop maupun perangkat mobile (dengan atau tanpa Bootstrap).
-   📂 **Struktur Proyek Modular:** Kode disusun dengan rapi agar mudah dipahami, dimodifikasi, dan dikembangkan lebih lanjut.

### 🏗️ Arsitektur Sistem

Sistem ini bekerja dengan alur sederhana namun efektif:

1.  **Perangkat Keras ASV (ESP32/RPi):** Mengumpulkan data GPS dan sensor lainnya.
2.  **Pengiriman Data:** Perangkat keras mengirimkan data dalam format JSON ke endpoint API di server Flask melalui koneksi HTTP (Wi-Fi/GSM).
3.  **Server Flask (Backend):** Menerima data, memprosesnya, dan menyimpannya (jika perlu). Server juga menyajikan halaman web utama.
4.  **Antarmuka Web (Frontend):** Secara periodik (misalnya, setiap beberapa detik), frontend mengambil data terbaru dari server menggunakan JavaScript (`fetch` API) dan memperbarui peta serta grafik tanpa perlu me-refresh halaman.

```
[ASV: ESP32/RPi] --(HTTP POST)--> [Server: Flask App] <--(Fetch API)-- [Client: Web Browser]
```

### 🛠️ Tumpukan Teknologi

| Kategori  | Teknologi                                      | Deskripsi                                 |
| :-------- | :--------------------------------------------- | :---------------------------------------- |
| **Backend** | Python 3.x, Flask                              | Logika server, routing, dan API endpoint. |
| **Frontend**| HTML5, CSS3, JavaScript (ES6+)                 | Struktur, gaya, dan interaktivitas.       |
| **Visualisasi** | Chart.js                                       | Membuat grafik data sensor yang dinamis.  |
| **Opsional** | Bootstrap 5, Leaflet.js / OpenStreetMap      | Desain responsif dan peta interaktif.     |

### 🚀 Instalasi & Konfigurasi

Untuk menjalankan proyek ini di lingkungan lokal, ikuti langkah-langkah berikut:

**1. Prasyarat**
* [Python 3.8+](https://www.python.org/downloads/)
* [Git](https://git-scm.com/)

**2. Kloning Repositori**
```bash
git clone [https://github.com/parull123/WEB-ASV.git](https://github.com/parull123/WEB-ASV.git)
cd WEB-ASV
```

**3. Buat dan Aktifkan Lingkungan Virtual (Virtual Environment)**
* Untuk Windows:
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```
* Untuk macOS/Linux:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

**4. Instalasi Dependensi**
```bash
pip install -r requirements.txt
```

**5. Jalankan Server Flask**
```bash
python app.py
```
Server akan berjalan di `http://127.0.0.1:5000`. Buka alamat ini di browser Anda.

### 📁 Struktur Proyek

```
WEB-ASV/
├── app.py              # File utama Flask (logika backend)
├── requirements.txt    # Daftar dependensi Python
├── static/
│   ├── css/
│   │   └── style.css   # File styling utama
│   └── js/
│       └── main.js     # Logika frontend (fetch data, update UI)
└── templates/
    └── index.html      # Halaman utama HTML
```

### 🔌 Endpoint API untuk Perangkat Keras

Perangkat keras (misalnya, ESP32) harus mengirimkan data sensor ke endpoint berikut menggunakan metode `POST`:

-   **URL:** `http://<IP_SERVER_ANDA>:5000/api/data`
-   **Metode:** `POST`
-   **Header:** `Content-Type: application/json`
-   **Body (Contoh JSON):**
    ```json
    {
      "gps": {
        "latitude": -6.2088,
        "longitude": 106.8456
      },
      "sensors": {
        "temperature": 28.5,
        "ph_level": 7.2
      }
    }
    ```

### 🤝 Kontribusi

Kontribusi dalam bentuk apapun sangat diterima! Jika Anda memiliki ide untuk fitur baru atau menemukan bug, silakan buat *Issue* atau kirim *Pull Request*.

1.  *Fork* repositori ini.
2.  Buat *branch* baru (`git checkout -b fitur/nama-fitur`).
3.  *Commit* perubahan Anda (`git commit -m 'Menambahkan fitur X'`).
4.  *Push* ke *branch* Anda (`git push origin fitur/nama-fitur`).
5.  Buat *Pull Request* baru.

### 📜 Lisensi

Proyek ini dilisensikan di bawah [Lisensi MIT](LICENSE).

---

### 👤 Pengembang

**Fahrul Ridho Dwinugroho**
* D4 Teknologi Rekayasa Otomasi - Angkatan 2022
* Universitas Negeri Jakarta
* Email: `fr.dwinugroho@gmail.com`
* GitHub: [@parull123](https://github.com/parull123)

---
---

## English Version <a name="english-version"></a>

### 📌 Key Features

-   🗺️ **Real-time Geospatial Monitoring:** Track the ASV's position live on an interactive map.
-   📊 **Sensor Data Visualization:** Display data from various sensors (e.g., temperature, humidity, water pH) in dynamic charts using Chart.js.
-   📡 **Two-Way Communication:** Designed to receive data from microcontrollers like **ESP32** or **Raspberry Pi** via an API endpoint.
-   📱 **Responsive Interface:** A user interface that works well on both desktop and mobile devices (with or without Bootstrap).
-   📂 **Modular Project Structure:** The code is neatly organized to be easy to understand, modify, and extend.

### 🏗️ System Architecture

The system operates on a simple yet effective workflow:

1.  **ASV Hardware (ESP32/RPi):** Collects GPS and other sensor data.
2.  **Data Transmission:** The hardware sends this data in JSON format to the Flask server's API endpoint via an HTTP connection (Wi-Fi/GSM).
3.  **Flask Server (Backend):** Receives the data, processes it, and stores it if necessary. The server also serves the main web page.
4.  **Web Interface (Frontend):** Periodically (e.g., every few seconds), the frontend fetches the latest data from the server using the JavaScript `fetch` API and updates the map and charts without requiring a page refresh.

```
[ASV: ESP32/RPi] --(HTTP POST)--> [Server: Flask App] <--(Fetch API)-- [Client: Web Browser]
```

### 🛠️ Technology Stack

| Category      | Technology                                     | Description                               |
| :------------ | :--------------------------------------------- | :---------------------------------------- |
| **Backend** | Python 3.x, Flask                              | Server logic, routing, and API endpoint.  |
| **Frontend** | HTML5, CSS3, JavaScript (ES6+)                 | Structure, styling, and interactivity.    |
| **Visualization** | Chart.js                                       | Creating dynamic sensor data charts.      |
| **Optional** | Bootstrap 5, Leaflet.js / OpenStreetMap      | Responsive design and interactive maps.   |

### 🚀 Installation & Setup

To run this project in your local environment, follow these steps:

**1. Prerequisites**
* [Python 3.8+](https://www.python.org/downloads/)
* [Git](https://git-scm.com/)

**2. Clone the Repository**
```bash
git clone [https://github.com/parull123/WEB-ASV.git](https://github.com/parull123/WEB-ASV.git)
cd WEB-ASV
```

**3. Create and Activate a Virtual Environment**
* For Windows:
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```
* For macOS/Linux:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

**4. Install Dependencies**
```bash
pip install -r requirements.txt
```

**5. Run the Flask Server**
```bash
python app.py
```
The server will be running at `http://127.0.0.1:5000`. Open this address in your browser.

### 📁 Project Structure

```
WEB-ASV/
├── app.py              # Main Flask file (backend logic)
├── requirements.txt    # List of Python dependencies
├── static/
│   ├── css/
│   │   └── style.css   # Main styling file
│   └── js/
│       └── main.js     # Frontend logic (fetch data, update UI)
└── templates/
    └── index.html      # Main HTML page
```

### 🔌 API Endpoint for Hardware

The hardware (e.g., ESP32) should send sensor data to the following endpoint using the `POST` method:

-   **URL:** `http://<YOUR_SERVER_IP>:5000/api/data`
-   **Method:** `POST`
-   **Header:** `Content-Type: application/json`
-   **Body (JSON Example):**
    ```json
    {
      "gps": {
        "latitude": -6.2088,
        "longitude": 106.8456
      },
      "sensors": {
        "temperature": 28.5,
        "ph_level": 7.2
      }
    }
    ```

### 🤝 Contributing

Contributions of any kind are welcome! If you have an idea for a new feature or find a bug, please create an *Issue* or submit a *Pull Request*.

1.  Fork this repository.
2.  Create a new branch (`git checkout -b feature/feature-name`).
3.  Commit your changes (`git commit -m 'Add feature X'`).
4.  Push to your branch (`git push origin feature/feature-name`).
5.  Create a new Pull Request.

### 📜 License

This project is licensed under the [MIT License](LICENSE).

---

### 👤 Developer

**Fahrul Ridho Dwinugroho**
* Automation Engineering Technology - Class of 2022
* State University of Jakarta (Universitas Negeri Jakarta)
* Email: `fr.dwinugroho@gmail.com`
* GitHub: [@parull123](https://github.com/parull123)
````
