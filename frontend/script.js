// ================= BASIC FUNCTIONS =================
let currentEvent = "all";
function goToFeedback() {
    window.location.href = "feedback.html";
}

function login() {
    const user = document.getElementById("username").value;
    const pass = document.getElementById("password").value;

    if (user === "admin" && pass === "1234") {
        localStorage.setItem("isLoggedIn", "true");
        window.location.href = "dashboard.html";
    } else {
        alert("Invalid credentials");
    }
}

// ================= GLOBAL VARIABLES =================

let allData = [];
let chartInstance;

// ================= DOM LOADED =================

document.addEventListener("DOMContentLoaded", () => {

    // ================= FEEDBACK FORM =================

    const form = document.getElementById("feedbackForm");
    loadEvents();

    if (form) {
        form.addEventListener("submit", async (e) => {
            e.preventDefault();

            const selectedEvent = document.getElementById("event").value;
            const customEvent = document.getElementById("customEvent")?.value;

            const data = {
                name: document.getElementById("name").value,
                event: customEvent ? customEvent : selectedEvent,
                rating: parseInt(document.getElementById("rating").value),
                comment: document.getElementById("comment").value
            };

            try {
                const response = await fetch("https://eventinsight-ai.onrender.com/submit", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(data)
                });

                const result = await response.json();

                alert("✅ Feedback Submitted! Sentiment: " + result.sentiment);
                form.reset();

            } catch (err) {
                alert("❌ Submission failed");
            }
        });
    }

    // ================= DASHBOARD =================

    if (document.getElementById("table")) {
        loadData();
    }

    // ================= LIVE AI =================

    const liveInput = document.getElementById("liveInput");

    if (liveInput) {
        let timeout;

        liveInput.addEventListener("input", () => {

            clearTimeout(timeout);

            timeout = setTimeout(async () => {

                const text = liveInput.value;

                if (text.trim() === "") {
                    document.getElementById("liveSentiment").innerText = "---";
                    document.getElementById("liveKeywords").innerText = "---";
                    return;
                }

                try {
                    const response = await fetch("https://eventinsight-ai.onrender.com/analyze", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ comment: text })
                    });

                    const result = await response.json();

                    const sentimentEl = document.getElementById("liveSentiment");
                    sentimentEl.innerText = result.sentiment;

                    // Color sentiment
                    if (result.sentiment === "positive") {
                        sentimentEl.style.color = "#22c55e";
                    } else if (result.sentiment === "negative") {
                        sentimentEl.style.color = "#ef4444";
                    } else {
                        sentimentEl.style.color = "#eab308";
                    }

                    // Keywords styling
                    const keywordsArray = result.keywords.split(",");

                    const positiveWords = ["good", "excellent", "nice", "best"];
                    const negativeWords = ["bad", "worst", "poor", "terrible"];

                    let styledKeywords = keywordsArray.map(word => {

                        const clean = word.trim().toLowerCase();

                        if (positiveWords.includes(clean)) {
                            return `<span class="kw-positive">${clean}</span>`;
                        } else if (negativeWords.includes(clean)) {
                            return `<span class="kw-negative">${clean}</span>`;
                        } else {
                            return `<span class="kw-neutral">${clean}</span>`;
                        }
                    });

                    document.getElementById("liveKeywords").innerHTML =
                        styledKeywords.join(", ");

                } catch (err) {
                    console.log("Live AI failed");
                }

            }, 400);
        });
    }

    // ================= CUSTOM EVENT SHOW =================

    const eventDropdown = document.getElementById("event");
    const customInput = document.getElementById("customEvent");

    if (eventDropdown && customInput) {
        eventDropdown.addEventListener("change", () => {
            if (eventDropdown.value === "Other") {
                customInput.style.display = "block";
            } else {
                customInput.style.display = "none";
                customInput.value = "";
            }
        });
    }

});


// ================= LOAD DATA =================

async function loadData() {

    const loader = document.getElementById("loader");
    if (loader) loader.style.display = "block";

    try {
        allData = [];

        const response = await fetch("https://eventinsight-ai.onrender.com/feedback");
        allData = await response.json();

        populateDropdown();
        renderDashboard("all");

    } catch (err) {
        console.error("Load failed", err);
    }

    if (loader) loader.style.display = "none";
}


// ================= EVENTS DROPDOWN =================

async function loadEvents() {
    const response = await fetch("https://eventinsight-ai.onrender.com/feedback");
    const data = await response.json();

    const dropdown = document.getElementById("event");
    if (!dropdown) return;

    const events = [...new Set(data.map(item => item.event))];
    dropdown.innerHTML = '<option value="">Select Event</option>';

events.forEach(event => {
    dropdown.innerHTML += `<option value="${event}">${event}</option>`;
});

    // Add preset + Other
    const preset = ["Tech Fest", "Music Fest", "Food Fest", "Workshop", "Seminar"];

    preset.forEach(ev => {
        if (!events.includes(ev)) {
            dropdown.innerHTML += `<option value="${ev}">${ev}</option>`;
        }
    });

    dropdown.innerHTML += `<option value="Other">Other</option>`;
}


// ================= EVENT FILTER =================

function populateDropdown() {
    const dropdown = document.getElementById("eventFilter");

    if (!dropdown) return;

    const events = [...new Set(allData.map(item => item.event))];

    dropdown.innerHTML = `<option value="all">All Events</option>`;

    events.forEach(event => {
        dropdown.innerHTML += `<option value="${event}">${event}</option>`;
    });

    dropdown.onchange = (e) => {
    renderDashboard(e.target.value);
};
}


// ================= DASHBOARD =================

function renderDashboard(selectedEvent) {

    const table = document.querySelector("#table tbody");
    table.innerHTML = "";

    let filteredData = selectedEvent === "all"
        ? allData
        : allData.filter(item => item.event === selectedEvent);

    let total = filteredData.length;
    let positive = 0;
    let negative = 0;

    filteredData.forEach(item => {

        if (item.sentiment === "positive") positive++;
        if (item.sentiment === "negative") negative++;

        table.innerHTML += `
            <tr>
                <td>${item.name}</td>
                <td>${item.event}</td>
                <td>${item.rating}</td>
                <td>${item.comment}</td>
                <td>${item.sentiment}</td>
                <td>${item.keywords}</td>
            </tr>
        `;
    });

    document.getElementById("total").innerText = total;
    document.getElementById("positive").innerText = positive;
    document.getElementById("negative").innerText = negative;

    updateChart(positive, negative);

    // 🚀 NEW SMART LOADING (NO FREEZE)
    loadAIPanels(selectedEvent);
}
async function safeFetch(url) {
    try {
        const controller = new AbortController();
        const timeout = setTimeout(() => controller.abort(), 5000);

        const res = await fetch(url, { signal: controller.signal });
        clearTimeout(timeout);

        return await res.json();
    } catch (err) {
        console.log("API failed:", url);
        return null;
    }
}

async function loadAIPanels(selectedEvent) {

    const requestEvent = selectedEvent;
    currentEvent = selectedEvent;

    document.getElementById("aiSummary").innerText = "Loading...";
    document.getElementById("successRate").innerText = "...";
    document.getElementById("predictionText").innerText = "...";
    document.getElementById("confidenceLevel").innerText = "...";

    // ===== SUMMARY =====
    const summary = await safeFetch(`https://eventinsight-ai.onrender.com/summary?event=${selectedEvent}`);
    if (currentEvent !== requestEvent) return;

    if (summary && summary.summary) {
        document.getElementById("aiSummary").innerText = summary.summary;
    } else {
        document.getElementById("aiSummary").innerText = "⚠️ Not enough data for this event";
    }

    // ===== PREDICTION =====
    const prediction = await safeFetch(`https://eventinsight-ai.onrender.com/predict?event=${selectedEvent}`);
    if (currentEvent !== requestEvent) return;

    if (prediction) {
        let rate = prediction.success_rate;

        if (typeof rate === "string") {
            rate = rate.replace("%", "");
        }

        rate = parseFloat(rate);

        document.getElementById("successRate").innerText =
    isNaN(rate) ? "--" : Math.round(rate) + "%";

        document.getElementById("predictionText").innerText =
            prediction.prediction || "Not enough data";

        document.getElementById("confidenceLevel").innerText =
            prediction.confidence || "--";
    }

    // ===== SUGGESTIONS =====
    const suggestions = await safeFetch(`https://eventinsight-ai.onrender.com/suggestions?event=${selectedEvent}`);
    if (currentEvent !== requestEvent) return;

    const suggestionList = document.getElementById("suggestionList");
    suggestionList.innerHTML = "";

    if (suggestions && suggestions.suggestions?.length) {
        suggestions.suggestions.forEach(item => {
            suggestionList.innerHTML += `<li>${item}</li>`;
        });
    } else {
        suggestionList.innerHTML = "<li>👍 No major issues detected</li>";
    }

    // ===== INSIGHTS =====
    const insights = await safeFetch(`https://eventinsight-ai.onrender.com/event-insights?event=${selectedEvent}`);
    if (currentEvent !== requestEvent) return;

    if (insights) {
        document.getElementById("bestEvent").innerText = insights.best_event;
        document.getElementById("worstEvent").innerText = insights.worst_event;
        document.getElementById("avgRating").innerText = insights.avg_rating;
        document.getElementById("riskLevel").innerText = insights.risk;
    }
}


// ================= CHART =================

function updateChart(positive, negative) {

    const ctx = document.getElementById('sentimentChart').getContext('2d');

    if (chartInstance) chartInstance.destroy();

    if (positive === 0 && negative === 0) positive = 1;

    chartInstance = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['Positive', 'Negative'],
            datasets: [{
                data: [positive, negative],
                backgroundColor: ['#22c55e', '#ef4444'],
                borderWidth: 2,
                borderColor: "#1e293b"
            }]
        },
        options: {
            responsive: true,
    maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: { color: "#fff" }
                }
            }
        }
    });
}


// ================= EXPORT CSV =================

function exportCSV() {

    let csv = "Name,Event,Rating,Comment,Sentiment,Keywords\n";

    document.querySelectorAll("#table tbody tr").forEach(row => {
        let cols = row.querySelectorAll("td");
        let rowData = [];

        cols.forEach(col => rowData.push(col.innerText));

        csv += rowData.join(",") + "\n";
    });

    const blob = new Blob([csv], { type: "text/csv" });
    const url = window.URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "feedback.csv";
    a.click();
}
document.getElementById("event").addEventListener("change", function () {
    const customBox = document.getElementById("customEventBox");

    if (this.value === "Other") {
        customBox.style.display = "block";
    } else {
        customBox.style.display = "none";
    }
});
const stars = document.querySelectorAll(".stars span");
const ratingInput = document.getElementById("rating");

stars.forEach(star => {
    star.addEventListener("click", () => {
        let val = star.getAttribute("data-value");
        ratingInput.value = val;

        stars.forEach(s => s.classList.remove("active"));

        for (let i = 0; i < val; i++) {
            stars[i].classList.add("active");
        }
    });
});