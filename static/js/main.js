/**
 * Smart Resume Analyzer - Interactive Frontend Controller
 * Handles Chart.js visualizations, file drag-and-drop, and dynamic role re-calculation.
 */

document.addEventListener("DOMContentLoaded", () => {
    // -------------------------------------------------------------
    // 1. File Upload & Drag-and-Drop Interaction
    // -------------------------------------------------------------
    const dropArea = document.getElementById("dropArea");
    const fileInput = document.getElementById("fileInput");
    const fileLabel = document.getElementById("fileLabel");
    const fileSelectedInfo = document.getElementById("fileSelectedInfo");

    if (dropArea && fileInput) {
        ["dragenter", "dragover", "dragleave", "drop"].forEach(eventName => {
            dropArea.addEventListener(eventName, preventDefaults, false);
            document.body.addEventListener(eventName, preventDefaults, false);
        });

        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }

        ["dragenter", "dragover"].forEach(eventName => {
            dropArea.addEventListener(eventName, () => dropArea.classList.add("dragover"), false);
        });

        ["dragleave", "drop"].forEach(eventName => {
            dropArea.addEventListener(eventName, () => dropArea.classList.remove("dragover"), false);
        });

        dropArea.addEventListener("drop", (e) => {
            const dt = e.dataTransfer;
            const files = dt.files;
            if (files.length) {
                fileInput.files = files;
                updateFileInfo(files[0]);
            }
        });

        fileInput.addEventListener("change", (e) => {
            if (e.target.files.length) {
                updateFileInfo(e.target.files[0]);
            }
        });

        function updateFileInfo(file) {
            if (fileLabel) fileLabel.textContent = file.name;
            if (fileSelectedInfo) {
                fileSelectedInfo.classList.remove("d-none");
                fileSelectedInfo.innerHTML = `<i class="fa-solid fa-file-check me-1"></i> Ready: ${file.name} (${(file.size / 1024).toFixed(1)} KB)`;
            }
        }
    }

    // -------------------------------------------------------------
    // 2. Dashboard Charts Initialization
    // -------------------------------------------------------------
    if (window.dashboardData) {
        initDashboardCharts(window.dashboardData);
    }

    // -------------------------------------------------------------
    // 3. Dynamic Target Role Switcher (Live Recalculation)
    // -------------------------------------------------------------
    const switchRoleSelect = document.getElementById("switchRoleSelect");
    if (switchRoleSelect) {
        switchRoleSelect.addEventListener("change", async (e) => {
            const newRole = e.target.value;
            const analysisId = switchRoleSelect.getAttribute("data-analysis-id");

            try {
                const response = await fetch("/api/recalculate", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ analysis_id: analysisId, target_role: newRole })
                });

                if (response.ok) {
                    const data = await response.json();
                    updateDashboardWithNewRole(data.ats, data.feedback);
                } else {
                    console.error("Failed to recalculate ATS score.");
                }
            } catch (err) {
                console.error("Error communicating with server:", err);
            }
        });
    }
});

let resumeScoreChart = null;
let atsScoreChart = null;
let breakdownBarChart = null;
let skillsDonutChart = null;

function initDashboardCharts(data) {
    const resumeCtx = document.getElementById("resumeScoreChart")?.getContext("2d");
    const atsCtx = document.getElementById("atsScoreChart")?.getContext("2d");
    const barCtx = document.getElementById("breakdownBarChart")?.getContext("2d");
    const donutCtx = document.getElementById("skillsDonutChart")?.getContext("2d");

    // Circular Resume Score Gauge
    if (resumeCtx) {
        resumeScoreChart = new Chart(resumeCtx, {
            type: "doughnut",
            data: {
                datasets: [{
                    data: [data.resumeScore, Math.max(0, 100 - data.resumeScore)],
                    backgroundColor: ["#6366f1", "rgba(255, 255, 255, 0.05)"],
                    borderWidth: 0,
                    borderRadius: 8
                }]
            },
            options: {
                cutout: "80%",
                responsive: true,
                maintainAspectRatio: false,
                plugins: { tooltip: { enabled: false } }
            }
        });
    }

    // Circular ATS Compatibility Gauge
    if (atsCtx) {
        atsScoreChart = new Chart(atsCtx, {
            type: "doughnut",
            data: {
                datasets: [{
                    data: [data.atsScore, Math.max(0, 100 - data.atsScore)],
                    backgroundColor: [data.atsScore >= 75 ? "#10b981" : data.atsScore >= 50 ? "#3b82f6" : "#f59e0b", "rgba(255, 255, 255, 0.05)"],
                    borderWidth: 0,
                    borderRadius: 8
                }]
            },
            options: {
                cutout: "80%",
                responsive: true,
                maintainAspectRatio: false,
                plugins: { tooltip: { enabled: false } }
            }
        });
    }

    // Parameter Breakdown Bar Chart
    if (barCtx) {
        const b = data.breakdown || {};
        breakdownBarChart = new Chart(barCtx, {
            type: "bar",
            data: {
                labels: ["Contact (15)", "Structure (20)", "Skills (20)", "Experience (15)", "Projects (15)", "Education (15)"],
                datasets: [{
                    label: "Score Earned",
                    data: [
                        b.contact_score || 0,
                        b.structure_score || 0,
                        b.skills_score || 0,
                        b.experience_score || 0,
                        b.projects_score || 0,
                        b.education_score || 0
                    ],
                    backgroundColor: [
                        "#06b6d4",
                        "#6366f1",
                        "#8b5cf6",
                        "#ec4899",
                        "#10b981",
                        "#f59e0b"
                    ],
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 20,
                        grid: { color: "rgba(255, 255, 255, 0.05)" },
                        ticks: { color: "#94a3b8" }
                    },
                    x: {
                        grid: { display: false },
                        ticks: { color: "#94a3b8", font: { size: 10 } }
                    }
                },
                plugins: {
                    legend: { display: false }
                }
            }
        });
    }

    // Skills Keyword Distribution Donut
    if (donutCtx) {
        skillsDonutChart = new Chart(donutCtx, {
            type: "doughnut",
            data: {
                labels: ["Matched Core", "Matched Secondary", "Missing Core", "Missing Secondary"],
                datasets: [{
                    data: [
                        data.matchedCoreCount || 0,
                        data.matchedSecondaryCount || 0,
                        data.missingCoreCount || 0,
                        data.missingSecondaryCount || 0
                    ],
                    backgroundColor: ["#10b981", "#3b82f6", "#ef4444", "#f59e0b"],
                    borderWidth: 2,
                    borderColor: "#0f172a"
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: "right",
                        labels: { color: "#cbd5e1", font: { size: 11 }, boxWidth: 12 }
                    }
                }
            }
        });
    }
}

function updateDashboardWithNewRole(ats, feedback) {
    // 1. Update text displays
    const displayAtsScore = document.getElementById("displayAtsScore");
    if (displayAtsScore) displayAtsScore.textContent = `${ats.ats_score}%`;

    const displayRoleName = document.getElementById("displayRoleName");
    if (displayRoleName) displayRoleName.textContent = ats.role_name;

    const displayMatchedCount = document.getElementById("displayMatchedCount");
    if (displayMatchedCount) displayMatchedCount.textContent = ats.total_matched;

    const roleTitleHeader = document.getElementById("roleTitleHeader");
    if (roleTitleHeader) roleTitleHeader.textContent = ats.role_title;

    const roleCategoryBadge = document.getElementById("roleCategoryBadge");
    if (roleCategoryBadge) roleCategoryBadge.textContent = ats.role_category;

    const roleDescText = document.getElementById("roleDescText");
    if (roleDescText) roleDescText.textContent = ats.role_description;

    // 2. Update ATS score gauge
    if (atsScoreChart) {
        const color = ats.ats_score >= 75 ? "#10b981" : ats.ats_score >= 50 ? "#3b82f6" : "#f59e0b";
        atsScoreChart.data.datasets[0].data = [ats.ats_score, Math.max(0, 100 - ats.ats_score)];
        atsScoreChart.data.datasets[0].backgroundColor = [color, "rgba(255, 255, 255, 0.05)"];
        atsScoreChart.update();
    }

    // 3. Update Skills Donut Chart
    if (skillsDonutChart) {
        skillsDonutChart.data.datasets[0].data = [
            ats.matched_core.length,
            ats.matched_secondary.length,
            ats.missing_core.length,
            ats.missing_secondary.length
        ];
        skillsDonutChart.update();
    }

    // 4. Update Matched & Missing skill tags
    renderTags("matchedCoreContainer", ats.matched_core, "matched", "fa-check");
    renderTags("matchedSecondaryContainer", ats.matched_secondary, "secondary", "fa-check");
    renderTags("missingCoreContainer", ats.missing_core, "missing", "fa-plus");
    renderTags("missingSecondaryContainer", ats.missing_secondary, "warning-tag", "fa-plus");

    // 5. Update Feedback Items
    const feedbackContainer = document.getElementById("feedbackContainer");
    if (feedbackContainer && feedback) {
        feedbackContainer.innerHTML = feedback.map(item => `
            <div class="feedback-card priority-${item.priority}">
                <div class="d-flex align-items-start justify-content-between gap-3">
                    <div class="d-flex align-items-start gap-3">
                        <div class="p-2 rounded-3 bg-dark text-${item.color} mt-1">
                            <i class="fa-solid ${item.icon}"></i>
                        </div>
                        <div>
                            <div class="d-flex align-items-center gap-2 mb-1">
                                <h6 class="text-white fw-bold mb-0">${item.title}</h6>
                                <span class="badge bg-${item.color} bg-opacity-25 text-${item.color} small" style="font-size: 0.7rem;">
                                    ${item.priority} Priority
                                </span>
                            </div>
                            <p class="text-secondary small mb-0">${item.description}</p>
                        </div>
                    </div>
                    <span class="badge bg-secondary-subtle text-secondary small text-nowrap d-none d-md-inline-block">
                        ${item.category}
                    </span>
                </div>
            </div>
        `).join("");
    }
}

function renderTags(containerId, list, typeClass, iconClass) {
    const el = document.getElementById(containerId);
    if (!el) return;
    if (!list || list.length === 0) {
        el.innerHTML = `<span class="text-muted small">None</span>`;
        return;
    }
    el.innerHTML = list.map(item => `
        <span class="skill-tag ${typeClass}">
            <i class="fa-solid ${iconClass}"></i> ${item.charAt(0).toUpperCase() + item.slice(1)}
        </span>
    `).join("");
}
