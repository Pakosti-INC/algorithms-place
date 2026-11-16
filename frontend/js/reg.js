document.addEventListener('DOMContentLoaded', () => {
    const regForm = document.getElementById('reg-form');
    if (!regForm) return;

    regForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const lastName = document.getElementById('last-name').value.trim();
        const firstName = document.getElementById('first-name').value.trim();
        const middleName = document.getElementById('middle-name').value.trim();
        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value;
        const errorMsg = document.getElementById('error-msg');

        errorMsg.classList.add('hidden');

        const payload = {
            email: email,
            first_name: firstName,
            middle_name: middleName || '',
            last_name: lastName,
            password: password,
        };

        try {
            const response = await fetch('http://127.0.0.1:8000/auth/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            const data = await response.json();

            if (!response.ok) {
                errorMsg.innerText = data.detail || 'Ошибка при регистрации';
                errorMsg.classList.remove('hidden');
                return;
            }

            window.location.href = 'login.html';
        } catch (err) {
            errorMsg.innerText = 'Ошибка соединения с сервером';
            errorMsg.classList.remove('hidden');
            console.error(err);
        }
    });
});