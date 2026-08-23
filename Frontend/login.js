document.getElementById('loginForm').addEventListener('submit', function (e) {
    e.preventDefault();

    const usn = document.getElementById('username').value;
    const psw = document.getElementById('password').value;
    const errorMsg = document.getElementById('errorMsg');
     
    if (usn === 'Cmr' && psw === 'Cmr123') {

        window.location.href = 'questionnaire.html';
    } else {
        errorMsg.classList.remove('hidden');
    }
});
