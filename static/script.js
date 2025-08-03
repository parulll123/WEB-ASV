document.addEventListener('DOMContentLoaded', function () {
    // === SELEKSI ELEMEN DOM ===
    const batteryLevelSpan = document.getElementById('battery-level');
    const sogValueSpan = document.getElementById('sog-value');
    const cogValueSpan = document.getElementById('cog-value');
    const geoTableBody = document.querySelector('.boat-tracker table tbody');
    const prepStatusSpan = document.getElementById('prep-status');
    const startStatusSpan = document.getElementById('start-status');
    const ballCountSpan = document.getElementById('ball-count');
    const surfaceImgStatusSpan = document.getElementById('surface-img-status');
    const underwaterImgStatusSpan = document.getElementById('underwater-img-status');
    const finishStatusSpan = document.getElementById('finish-status');
    
    // === SETUP PETA LEAFLET ===
    // Inisialisasi peta dan atur view awal (misal: Jakarta) dan level zoom
    const map = L.map('map').setView([-6.20, 106.81], 13);

    // Tambahkan 'tile layer' (gambar peta dasar) dari OpenStreetMap
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    // Variabel untuk menyimpan marker dan jejak (polyline)
    let boatMarker = null;
    let trajectoryPath = null;


    // === FUNGSI UTAMA PENGAMBIL DATA ===
    async function fetchData() {
        try {
            const response = await fetch('/data');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();

            // 1. Update Position-Log
            prepStatusSpan.textContent = data.position_log.preparation ? '✅ Completed' : 'Waiting...';
            startStatusSpan.textContent = data.position_log.start ? '✅ Started' : 'Waiting...';
            ballCountSpan.textContent = data.position_log.floating_ball_set;
            surfaceImgStatusSpan.textContent = data.position_log.mission_surface_imaging ? '✅ Completed' : 'Waiting...';
            underwaterImgStatusSpan.textContent = data.position_log.mission_underwater_imaging ? '✅ Completed' : 'Waiting...';
            finishStatusSpan.textContent = data.position_log.finish ? '✅ Finished' : 'Waiting...';

            // 2. Update Attitude Information
            sogValueSpan.textContent = data.attitude_info.sog.toFixed(2) + ' knots';
            cogValueSpan.textContent = data.attitude_info.cog.toFixed(2) + ' degrees';

            // 3. Update Other Indicators
            batteryLevelSpan.textContent = data.other_indicators.battery_level + ' %';
            
            // 4. Update Geo-tag Info Table
            geoTableBody.innerHTML = '';
            data.geo_tags.forEach((entry, index) => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${index + 1}</td>
                    <td>${entry.timestamp}</td>
                    <td>${entry.latitude.toFixed(6)}, ${entry.longitude.toFixed(6)}</td>
                    <td>${entry.sog.toFixed(2)}</td>
                    <td>${entry.cog.toFixed(2)} &deg;</td>
                `;
                geoTableBody.appendChild(row);
            });
            
            // 5. Update Peta (Marker dan Jejak)
            const trajectoryPoints = data.attitude_info.trajectory;
            if (trajectoryPoints.length > 0) {
                const latestPoint = trajectoryPoints[trajectoryPoints.length - 1];
                const latestLatLng = [latestPoint[0], latestPoint[1]];

                // Update Penanda (Marker)
                if (!boatMarker) {
                    boatMarker = L.marker(latestLatLng).addTo(map)
                        .bindPopup('Posisi Kapal Saat Ini.');
                } else {
                    boatMarker.setLatLng(latestLatLng);
                }

                // Update Jejak (Polyline)
                if (!trajectoryPath) {
                    trajectoryPath = L.polyline(trajectoryPoints, { color: 'blue' }).addTo(map);
                } else {
                    trajectoryPath.setLatLngs(trajectoryPoints);
                }

                // Atur view peta agar selalu mengikuti marker
                map.setView(latestLatLng, 16);
            }

        } catch (error) {
            console.error('Error fetching data:', error);
        }
    }

    // === MEMULAI FETCH DATA SECARA BERKALA ===
    fetchData(); // Panggil pertama kali saat halaman dimuat
    const intervalId = setInterval(fetchData, 2000); // Set interval untuk update setiap 2 detik

    // Membersihkan interval saat halaman ditutup untuk mencegah memory leak
    window.addEventListener('beforeunload', function () {
        clearInterval(intervalId);
    });
});