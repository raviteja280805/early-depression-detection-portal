let currentStep = 1;
const totalSteps = 6;


document.addEventListener('DOMContentLoaded', () => {
    updateProgress();
});

function updateProgress() {
    const progress = (currentStep / totalSteps) * 100;
    document.getElementById('progressBar').style.width = `${progress}%`;
    document.getElementById('stepCount').innerText = `Step ${currentStep} of ${totalSteps}`;
}

function nextStep(step) {
    const currentStepDiv = document.getElementById(`step${step}`);

   
    if (step === 1) {
        const name = document.getElementById('userName').value.trim();
        const age = document.getElementById('userAge').value;
        if (!name || !age) {
            alert("Please enter your name and age.");
            return;
        }
    }
    else {
        
        const radios = currentStepDiv.querySelectorAll('input[type="radio"]');
        const names = new Set();
        radios.forEach(r => names.add(r.name));

        for (let name of names) {
            const checked = currentStepDiv.querySelector(`input[name="${name}"]:checked`);
            if (!checked) {
                alert("Please answer all questions in this step.");
                return;
            }
        }
    }

    
    document.getElementById(`step${step}`).classList.remove('active');
    currentStep++;
    document.getElementById(`step${currentStep}`).classList.add('active');
    updateProgress();
}

function prevStep(step) {
    document.getElementById(`step${step}`).classList.remove('active');
    currentStep--;
    document.getElementById(`step${currentStep}`).classList.add('active');
    updateProgress();
}

function getRadioValue(name) {
    const el = document.querySelector(`input[name="${name}"]:checked`);
    return el ? parseInt(el.value) : null;
}

document.getElementById('quizForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    const text = document.getElementById('userInput').value;
    if (!text) {
        alert("Please describe how you feel.");
        return;
    }

    
    const payload = {
        name: document.getElementById('userName').value.trim(),
        age: parseInt(document.getElementById('userAge').value),
        text: text,

        q1_mood: getRadioValue('q1_mood'),
        q2_anxiety: getRadioValue('q2_anxiety'),
        q3_irritability: getRadioValue('q3_irritability'),
        q4_stress: getRadioValue('q4_stress'),
        q5_overthinking: getRadioValue('q5_overthinking'),
        q6_sleep: getRadioValue('q6_sleep'),
        q7_energy: getRadioValue('q7_energy'),
        q8_work_pressure: getRadioValue('q8_work_pressure'),
        q9_focus: getRadioValue('q9_focus'),
        q10_social: getRadioValue('q10_social'),
        q11_activities: getRadioValue('q11_activities'),
        q12_future: getRadioValue('q12_future')
    };

    
    const submitBtn = document.getElementById('submitBtn');
    const loading = document.getElementById('loading');

    
    submitBtn.disabled = true;
    submitBtn.innerText = "Analyzing...";
    loading.classList.remove('hidden');
    
    loading.innerHTML = '<div style="font-weight: 600; color: #42a5f5;">Analyzing your responses...</div>';

    try {
        
        const response = await fetch('http://127.0.0.1:8000/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!response.ok) throw new Error('API Error');

        const data = await response.json();
        localStorage.setItem('analysisResult', JSON.stringify(data));
        window.location.href = 'result.html';

    } catch (error) {
        console.error(error);

        
        submitBtn.disabled = false;
        submitBtn.innerText = "Try Again";
        loading.innerHTML = `<div style="font-weight: 600; color: #f44336;">Server connection failed. Please try again.</div>`;
    }
});
