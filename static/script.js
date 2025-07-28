document.addEventListener('DOMContentLoaded', function () {
    // === SELEKSI ELEMEN ===
    const batteryLevelSpan = document.getElementById('battery-level');
    const sogValueSpan = document.getElementById('sog-value');
    const cogValueSpan = document.getElementById('cog-value');
    const visualVideoIframe = document.getElementById('visual-video');

    const prepStatusSpan = document.getElementById('prep-status');
    const startStatusSpan = document.getElementById('start-status');
    const ballCountSpan = document.getElementById('ball-count');
    const surfaceImgStatusSpan = document.getElementById('surface-img-status');
    const underwaterImgStatusSpan = document.getElementById('underwater-img-status');
    const finishStatusSpan = document.getElementById('finish-status');
    
    const geoTableBody = document.querySelector('.boat-tracker table tbody');

    // === SETUP CHART.JS ===
    const ctx = document.getElementById('trajectoryChart').getContext('2d');
    const trajectoryChart = new Chart(ctx, {
        type: 'line', // Menggunakan tipe 'line' untuk plot Lat/Lon
        data: {
            datasets: [{
                label: 'Trajectory',
                data: [], // Data akan dalam format {x: longitude, y: latitude}
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1,
                fill: false,
                showLine: true // Pastikan garis terlihat
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    type: 'linear',
                    title: {
                        display: true,
                        text: 'Longitude'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Latitude'
                    }
                }
            }
        }
    });

    // === FUNGSI UTAMA PENGAMBIL DATA ===
    async function fetchData() {
        try {
            const response = await fetch('/data'); // Mengambil data dari endpoint Flask /data
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

            // 3. Update Trajectory Chart
            const trajectoryPoints = data.attitude_info.trajectory.map(point => ({
                x: point[0], // longitude
                y: point[1]  // latitude
            }));
            trajectoryChart.data.datasets[0].data = trajectoryPoints;
            trajectoryChart.update('none'); // 'none' untuk update tanpa animasi agar lebih mulus

            // 4. Update Other Indicators
            batteryLevelSpan.textContent = data.other_indicators.battery_level + ' %';
            if (!visualVideoIframe.src.endsWith(data.other_indicators.visual_video_url)) {
                visualVideoIframe.src = data.other_indicators.visual_video_url;
            }

            // 5. Update Geo-tag Info Table (DIPINDAHKAN KE SINI)
            // Bagian ini sekarang akan berjalan setiap kali data baru diterima
            geoTableBody.innerHTML = ''; // Kosongkan tabel sebelum diisi ulang
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

        } catch (error) {
            console.error('Error fetching data:', error);
            // Anda bisa menambahkan notifikasi error di UI di sini jika perlu
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

// KODE DI BAWAH INI DIHAPUS KARENA SALAH DAN REDUNDAN
// setInterval(fetchData, 5000); 
// }