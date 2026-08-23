document.addEventListener('DOMContentLoaded', function () {
    const dataStr = localStorage.getItem('analysisResult');

    if (!dataStr) {
        window.location.href = 'questionnaire.html';
        return;
    }

    const data = JSON.parse(dataStr);

    
    const riskScore = data.final_score; 
    let wellnessScore = 100 - riskScore;

   
    animateValue('finalScore', 0, wellnessScore, 1000);
    document.getElementById('finalCategory').innerText = data.category;

    
    const mainContainer = document.querySelector('.main-score-container');
    let themeColor = '#4caf50';

    if (data.category === 'SEVERE') {
        themeColor = '#f44336';
    } else if (data.category === 'MODERATE') {
        themeColor = '#ff9800';
    } else if (data.category === 'NORMAL') {
        themeColor = '#4caf50';
    }

    mainContainer.style.border = `5px solid ${themeColor}`;
    document.getElementById('finalScore').style.color = themeColor;

    
    document.getElementById('aiSummaryText').innerHTML = data.summary;

    
    document.getElementById('adviceTitle').innerText = data.advice.title;

    const adviceListDiv = document.getElementById('adviceList');
    adviceListDiv.innerHTML = '';

    data.advice.steps.forEach((step, index) => {
        const item = document.createElement('div');
        item.className = 'insight-item';
        
        const icons = ['✓', '★', '➜', '❤'];
        const icon = icons[index % icons.length];

        item.innerHTML = `
            <div class="insight-icon">${icon}</div>
            <div class="insight-text">${step}</div>
        `;
        adviceListDiv.appendChild(item);
    });

    document.getElementById('downloadPdfBtn').addEventListener('click', function () {
        const element = document.querySelector('.container');
        const opt = {
            margin: 0.5,
            filename: 'Wellness_Summary.pdf',
            image: { type: 'jpeg', quality: 0.98 },
            html2canvas: { scale: 2 },
            jsPDF: { unit: 'in', format: 'letter', orientation: 'portrait' }
        };

        const buttonsDiv = document.getElementById('actionButtons');
        buttonsDiv.style.display = 'none';

        html2pdf().set(opt).from(element).save().then(() => {
            buttonsDiv.style.display = 'flex';
        });
    });
});


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
