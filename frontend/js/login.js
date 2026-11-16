document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    
    if (loginForm) {
        loginForm.addEventListener('submit', function(event) {
            event.preventDefault();
            // Эмуляция успешного входа и переход в основную систему
            window.location.href = 'index.html';
        });
    }
});

// Внутри login.js после получения data.access_token:
localStorage.setItem('token', data.access_token);

const payloadBase64 = data.access_token.split('.')[1].replace(/-/g, '+').replace(/_/g, '/');
const payload = JSON.parse(atob(payloadBase64));

if (payload.role === 'TEACHER') {
    window.location.href = 'teacher.html';
} else {
    window.location.href = 'index.html';
}