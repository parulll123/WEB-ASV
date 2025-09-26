// script.js - PERBAIKAN

document.addEventListener('DOMContentLoaded', function () {
    // === DOM ELEMENT SELECTION ===
    const batteryLevelSpan = document.getElementById('battery-level');
    const sogValueSpan = document.getElementById('sog-value');
    const cogValueSpan = document.getElementById('cog-value');
    const speedValueSpan = document.getElementById('speed-value');
    const geoTableBody = document.getElementById('geotag-tbody');
    const checklistTableBody = document.getElementById('checklist-tbody');

    // === LEAFLET MAP SETUP ===
    const map = L.map('map').setView([-6.20, 106.81], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    let boatMarker = null;
    let trajectoryPath = null;
    let geoTagCounter = 0;

    // === MAIN DATA FETCHING FUNCTION ===
    async function fetchData() {
        try {
            const response = await fetch('/data');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();

            // 1. Update Floating Ball Set Checklist
            if (data.floating_ball_checklist && checklistTableBody) {
                checklistTableBody.innerHTML = '';
                data.floating_ball_checklist.forEach(ball => {
                    const row = document.createElement('tr');
                    const statusText = ball.checked ? '✅ Checked' : '⌛ Waiting';
                    row.innerHTML = `
                        <td>${ball.id}</td>
                        <td>${statusText}</td>
                    `;
                    checklistTableBody.appendChild(row);
                });
            }

            // 2. Update Attitude Information (SOG, COG, Speed) and Quick Stats
            if (sogValueSpan) sogValueSpan.textContent = data.attitude_info.sog.toFixed(2);
            if (cogValueSpan) cogValueSpan.textContent = data.attitude_info.cog.toFixed(2);
            // PERBAIKAN: Tambahkan update untuk speed
            if (speedValueSpan) speedValueSpan.textContent = data.attitude_info.speed.toFixed(2);

            // 3. Update Other Indicators (Battery) and Quick Stats
            if (batteryLevelSpan) batteryLevelSpan.textContent = data.other_indicators.battery_level + ' %';

            // 4. Update Geo-tag Info Table
            if (data.geo_tags.length > 0 && geoTableBody) {
                const entry = data.geo_tags[0];
                geoTagCounter++;

                const row = document.createElement('tr');
                row.innerHTML = `
                <td>${geoTagCounter}</td>
                <td>${entry.timestamp}</td>
                <td>${entry.latitude.toFixed(6)}, ${entry.longitude.toFixed(6)}</td>
                <td>${entry.speed.toFixed(2)}</td>
                <td>${entry.sog.toFixed(2)}</td>
                <td>${entry.cog.toFixed(2)} &deg;</td>
            `;
                // PERBAIKAN: Ganti speedValueSpan dengan speed
                geoTableBody.prepend(row);

                const rows = geoTableBody.getElementsByTagName('tr');
                if (rows.length > 5) {
                    geoTableBody.removeChild(rows[rows.length - 1]);
                }
            }

            // 5. Update Map (Marker and Trajectory)
            const trajectoryPoints = data.attitude_info.trajectory;
            if (trajectoryPoints && trajectoryPoints.length > 0) {
                const latestPoint = trajectoryPoints[trajectoryPoints.length - 1];
                const latestLatLng = [latestPoint[0], latestPoint[1]];

                if (!boatMarker) {
                    boatMarker = L.marker(latestLatLng).addTo(map)
                        .bindPopup('Current Boat Position.');
                } else {
                    boatMarker.setLatLng(latestLatLng);
                }

                if (!trajectoryPath) {
                    trajectoryPath = L.polyline(trajectoryPoints, { color: '#00aaff', weight: 3 }).addTo(map);
                } else {
                    trajectoryPath.setLatLngs(trajectoryPoints);
                }
                map.setView(latestLatLng, 16);
            }

        } catch (error) {
            console.error('Error fetching data:', error);
        }
    }

    // === START PERIODIC DATA FETCHING ===
    fetchData();
    const intervalId = setInterval(fetchData, 2000);

    window.addEventListener('beforeunload', function () {
        clearInterval(intervalId);
    });
});