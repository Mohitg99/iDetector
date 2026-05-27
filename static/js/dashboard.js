document.addEventListener("DOMContentLoaded", () => {

    document.body.classList.remove("modal-open");

    document.body.style.overflow = "auto";

    document
        .querySelectorAll(".modal-backdrop")
        .forEach(el => el.remove());
});

let pieChart = null;
let lineChart = null;
let dashboardInterval = null;

// INITIALIZE CHARTS
function initCharts(resultData, dailyData) {

    const pieCanvas = document.getElementById("pieChart");
    const lineCanvas = document.getElementById("lineChart");

    if (!pieCanvas || !lineCanvas) {
        return;
    }

    // DESTROY OLD CHARTS
    if (pieChart) {
        pieChart.destroy();
    }

    if (lineChart) {
        lineChart.destroy();
    }

    // PIE CHART
    pieChart = new Chart(pieCanvas, {

        type: "pie",

        data: {

            labels: resultData.map(item => item[0]),

            datasets: [{
                data: resultData.map(item => item[1]),

                backgroundColor: [
                    "#22c55e",
                    "#ef4444"
                ],

                borderWidth: 2
            }]
        },

        options: {

            responsive: true,

            maintainAspectRatio: true,

            plugins: {
                legend: {
                    position: "top"
                }
            }
        }
    });

    // LINE CHART
    lineChart = new Chart(lineCanvas, {

        type: "line",

        data: {

            labels: dailyData.map(item => item[0]),

            datasets: [{

                label: "Violations",

                data: dailyData.map(item => item[1]),

                borderColor: "#2563eb",

                backgroundColor: "rgba(37,99,235,0.1)",

                fill: true,

                tension: 0.4,

                borderWidth: 3,

                pointRadius: 4
            }]
        },

        options: {

            responsive: true,

            maintainAspectRatio: true,

            plugins: {
                legend: {
                    display: true
                }
            },

            scales: {

                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// LOAD DASHBOARD DATA
async function loadDashboardData() {

    try {

        const response = await fetch("/api/dashboard-data");

        if (!response.ok) {
            throw new Error("Failed to load dashboard data");
        }

        const data = await response.json();

        // UPDATE STATS
        const total = document.getElementById("total");
        const mask = document.getElementById("mask");
        const nomask = document.getElementById("nomask");

        if (total) {
            total.innerText = data.images.length;
        }

        if (mask) {
            mask.innerText = data.stats.Mask || 0;
        }

        if (nomask) {
            nomask.innerText = data.stats["No Mask"] || 0;
        }

        // UPDATE IMAGE CARDS
        const container = document.getElementById("imageContainer");

        if (container) {

            container.innerHTML = "";

            data.images.forEach(item => {

                const resultClass =
                    item[1] === "Mask"
                        ? "text-success"
                        : "text-danger";

                container.innerHTML += `

                <div class="col-lg-4 col-md-6 mb-4">

                    <div class="card shadow border-0 rounded-4 overflow-hidden img-card">

                        <img 
                            src="/${item[0]}" 
                            class="card-img-top dashboard-img"
                            alt="Detection Image"
                        >

                        <div class="card-body text-center">

                            <h5 class="${resultClass}">
                                ${item[1]}
                            </h5>

                            <p class="fw-bold">
                                ${item[2]}
                            </p>

                            <small class="text-muted">
                                ${item[3]}
                            </small>

                        </div>

                    </div>

                </div>
                `;
            });
        }

        // UPDATE CHARTS
        initCharts(
            data.result_data,
            data.daily_data
        );

    } catch (error) {

        console.error("Dashboard Error:", error);
    }
}

// DARK MODE
function toggleDarkMode() {

    document.body.classList.toggle("dark-mode");

    const isDark =
        document.body.classList.contains("dark-mode");

    localStorage.setItem("darkMode", isDark);
}

// APPLY SAVED THEME
function applySavedTheme() {

    const darkMode =
        localStorage.getItem("darkMode");

    if (darkMode === "true") {

        document.body.classList.add("dark-mode");
    }
}

// PAGE LOAD
document.addEventListener("DOMContentLoaded", () => {

    applySavedTheme();

    // LOAD DATA FIRST TIME
    loadDashboardData();

    // CLEAR OLD INTERVAL
    if (dashboardInterval) {
        clearInterval(dashboardInterval);
    }

    // AUTO REFRESH
    dashboardInterval = setInterval(() => {

        // ONLY REFRESH IF USER IS STILL ON PAGE
        if (!document.hidden) {
            loadDashboardData();
        }

    }, 5000);
});

// STOP REFRESH WHEN LEAVING PAGE
window.addEventListener("beforeunload", () => {

    if (dashboardInterval) {
        clearInterval(dashboardInterval);
    }
});