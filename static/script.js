// script.js

document.addEventListener('DOMContentLoaded', function () {
    // === SELEKSI ELEMEN DOM ===
    const batteryLevelSpan = document.getElementById('battery-level'); // Asumsi ada elemen ini
    const sogValueSpan = document.getElementById('sog-value'); // Asumsi ada elemen ini
    const cogValueSpan = document.getElementById('cog-value'); // Asumsi ada elemen ini
    const geoTableBody = document.getElementById('geotag-tbody'); // Diperbaiki menggunakan ID
    const checklistTableBody = document.getElementById('checklist-tbody'); // Elemen baru untuk checklist

    // === SETUP PETA LEAFLET ===
    const map = L.map('map').setView([-6.20, 106.81], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    let boatMarker = null;
    let trajectoryPath = null;
    let geoTagCounter = 0; // Untuk penomoran tabel geo-tag

    // === FUNGSI UTAMA PENGAMBIL DATA ===
    async function fetchData() {
        try {
            const response = await fetch('/data');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();

            // 1. Update Floating Ball Set Checklist
            if (data.floating_ball_checklist && checklistTableBody) {
                checklistTableBody.innerHTML = ''; // Kosongkan tabel sebelum diisi
                data.floating_ball_checklist.forEach(ball => {
                    const row = document.createElement('tr');
                    const statusText = ball.checked ? '✅ Checked' : '❌ Waiting';
                    row.innerHTML = `
                        <td>${ball.id}</td>
                        <td>${statusText}</td>
                    `;
                    checklistTableBody.appendChild(row);
                });
            }

            // 2. Update Attitude Information (SOG, COG)
            // Pastikan elemen ini ada di HTML Anda jika ingin menampilkannya
            if (sogValueSpan) sogValueSpan.textContent = data.attitude_info.sog.toFixed(2) + ' knots';
            if (cogValueSpan) cogValueSpan.textContent = data.attitude_info.cog.toFixed(2) + ' degrees';

            // 3. Update Other Indicators (Baterai)
            // Pastikan elemen ini ada di HTML Anda
            if (batteryLevelSpan) batteryLevelSpan.textContent = data.other_indicators.battery_level + ' %';
            
            // 4. Update Geo-tag Info Table
            if (data.geo_tags.length > 0 && geoTableBody) {
                const entry = data.geo_tags[0]; // Ambil data geo-tag terbaru
                geoTagCounter++;

                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${geoTagCounter}</td>
                    <td>${entry.timestamp}</td>
                    <td>${entry.latitude.toFixed(6)}, ${entry.longitude.toFixed(6)}</td>
                    <td>${entry.sog.toFixed(2)}</td>
                    <td>${entry.cog.toFixed(2)} &deg;</td>
                `;
                // Tambahkan baris baru di atas, bukan di bawah
                geoTableBody.prepend(row); 
            }
            
            // 5. Update Peta (Marker dan Jejak)
            const trajectoryPoints = data.attitude_info.trajectory;
            if (trajectoryPoints && trajectoryPoints.length > 0) {
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
                map.setView(latestLatLng, 16);
            }

        } catch (error) {
            console.error('Error fetching data:', error);
        }
    }

    // === MEMULAI FETCH DATA SECARA BERKALA ===
    fetchData(); // Panggil pertama kali saat halaman dimuat
    const intervalId = setInterval(fetchData, 2000); // Update setiap 2 detik

    window.addEventListener('beforeunload', function () {
        clearInterval(intervalId);
    });
});