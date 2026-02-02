document.getElementById('loginForm').addEventListener('submit', function (e) {
    e.preventDefault();

    const usn = document.getElementById('username').value;
    const psw = document.getElementById('password').value;
    const errorMsg = document.getElementById('errorMsg');

    // Simple demo validation
    if (usn === 'Cmr' && psw === 'Cmr123') {
        // Redirect to questionnaire
        window.location.href = 'questionnaire.html';
    } else {
        errorMsg.classList.remove('hidden');
    }
});
