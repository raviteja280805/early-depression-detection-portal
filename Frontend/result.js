document.addEventListener('DOMContentLoaded', function () {
    const dataStr = localStorage.getItem('analysisResult');

    if (!dataStr) {
        window.location.href = 'questionnaire.html';
        return;
    }

    const data = JSON.parse(dataStr);

    // --- 1. Populate Main Score ---
    const riskScore = data.final_score; // 0 (Low Risk) to 100 (High Risk)
    // Convert to Wellness Score (0 = Bad, 100 = Good)
    let wellnessScore = 100 - riskScore;

    // Animate Number
    animateValue('finalScore', 0, wellnessScore, 1000);
    document.getElementById('finalCategory').innerText = data.category;

    // Color coding main score
    const mainContainer = document.querySelector('.main-score-container');
    let themeColor = '#4caf50'; // Green

    if (data.category.includes('High')) {
        themeColor = '#f44336';
    } else if (data.category.includes('Moderate')) {
        themeColor = '#ff9800';
    } else if (data.category.includes('Mild')) {
        themeColor = '#fbc02d';
    }

    mainContainer.style.border = `5px solid ${themeColor}`;
    document.getElementById('finalScore').style.color = themeColor;

    // --- 2. Detailed Summary ---
    document.getElementById('aiSummaryText').innerText = data.summary;

    // --- 3. Actionable Insights ---
    document.getElementById('adviceTitle').innerText = data.advice.title;

    const adviceListDiv = document.getElementById('adviceList');
    adviceListDiv.innerHTML = '';

    data.advice.steps.forEach((step, index) => {
        const item = document.createElement('div');
        item.className = 'insight-item';
        // Alternate icons for visual variety
        const icons = ['✓', '★', '➜', '❤'];
        const icon = icons[index % icons.length];

        item.innerHTML = `
            <div class="insight-icon">${icon}</div>
            <div class="insight-text">${step}</div>
        `;
        adviceListDiv.appendChild(item);
    });

});

// Helper: Animate Number Counting
function animateValue(id, start, end, duration) {
    const obj = document.getElementById(id);
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        obj.innerHTML = Math.floor(progress * (end - start) + start);
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
}
