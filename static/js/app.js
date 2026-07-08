// ===================================
// SIDEBAR TOGGLE (mobile)
// ===================================
function toggleSidebar() {
    const sidebar = document.getElementById("sidebar");
    if (sidebar) sidebar.classList.toggle("open");
}

// Close sidebar on outside click (mobile)
document.addEventListener("click", function (e) {
    const sidebar = document.getElementById("sidebar");
    const menuBtn = document.querySelector(".menu-btn");
    if (!sidebar || !menuBtn) return;
    if (!sidebar.contains(e.target) && !menuBtn.contains(e.target)) {
        sidebar.classList.remove("open");
    }
});


// ===================================
// AUTO-DISMISS ALERTS
// ===================================
setTimeout(() => {
    document.querySelectorAll(".alert").forEach(el => {
        el.style.transition = "opacity 0.5s";
        el.style.opacity = "0";
        setTimeout(() => el.remove(), 500);
    });
}, 4000);


// ===================================
// TOAST NOTIFICATION
// ===================================
function showToast(message, type = "info") {
    const toast = document.createElement("div");
    toast.className = "toast";
    toast.innerText = message;
    if (type === "error") toast.style.background = "#dc2626";
    if (type === "success") toast.style.background = "#16a34a";
    document.body.appendChild(toast);
    setTimeout(() => toast.classList.add("show"), 50);
    setTimeout(() => {
        toast.classList.remove("show");
        setTimeout(() => toast.remove(), 400);
    }, 3000);
}


// ===================================
// LIVE TABLE SEARCH (client-side)
// ===================================
const searchInputLive = document.querySelector(".search-box input[name='q']");
if (searchInputLive) {
    searchInputLive.addEventListener("input", function () {
        const val = this.value.toLowerCase().trim();
        const rows = document.querySelectorAll(".table tbody tr");
        rows.forEach(row => {
            row.style.display = row.innerText.toLowerCase().includes(val) ? "" : "none";
        });
    });
}


// ===================================
// ADMIN DASHBOARD CHART
// ===================================
const attCanvas = document.getElementById("attendanceChart");
if (attCanvas) {
    const labels  = attCanvas.dataset.labels  ? attCanvas.dataset.labels.split(",")  : [];
    const present = attCanvas.dataset.present ? attCanvas.dataset.present.split(",").map(Number) : [];
    const absent  = attCanvas.dataset.absent  ? attCanvas.dataset.absent.split(",").map(Number)  : [];

    new Chart(attCanvas, {
        type: "bar",
        data: {
            labels,
            datasets: [
                {
                    label: "Present",
                    data: present,
                    backgroundColor: "rgba(22,163,74,0.75)",
                    borderRadius: 5,
                },
                {
                    label: "Absent",
                    data: absent,
                    backgroundColor: "rgba(220,38,38,0.65)",
                    borderRadius: 5,
                }
            ]
        },
        options: {
            responsive: true,
            plugins: { legend: { position: "top" } },
            scales: { y: { beginAtZero: true, ticks: { stepSize: 1 } } }
        }
    });
}


// ===================================
// TEACHER DASHBOARD SUBJECT CHART
// ===================================
const subCanvas = document.getElementById("subjectChart");
if (subCanvas) {
    const labels = subCanvas.dataset.labels ? subCanvas.dataset.labels.split(",") : [];
    const avgs   = subCanvas.dataset.avgs   ? subCanvas.dataset.avgs.split(",").map(Number) : [];

    new Chart(subCanvas, {
        type: "bar",
        data: {
            labels,
            datasets: [{
                label: "Average Marks",
                data: avgs,
                backgroundColor: "rgba(37,99,235,0.7)",
                borderRadius: 6,
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { display: false } },
            scales: { y: { beginAtZero: true, max: 100 } }
        }
    });
}


// ===================================
// ATTENDANCE: SELECT ALL / NONE
// ===================================
const selectAllBtn = document.getElementById("selectAll");
const deselectAllBtn = document.getElementById("deselectAll");

if (selectAllBtn) {
    selectAllBtn.addEventListener("click", () => {
        document.querySelectorAll(".attendance-grid input[type='checkbox']").forEach(cb => cb.checked = true);
    });
}

if (deselectAllBtn) {
    deselectAllBtn.addEventListener("click", () => {
        document.querySelectorAll(".attendance-grid input[type='checkbox']").forEach(cb => cb.checked = false);
    });
}


// ===================================
// CONFIRM DELETE (via data attribute)
// ===================================
document.querySelectorAll("[data-confirm]").forEach(el => {
    el.addEventListener("click", function (e) {
        if (!confirm(this.dataset.confirm)) e.preventDefault();
    });
});
