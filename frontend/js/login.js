document.getElementById('login-form').addEventListener('submit', async function (event) {
    event.preventDefault(); // Отменяем стандартную перезагрузку страницы при отправке формы

    const email = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value;
    const errorMsg = document.getElementById('error-msg');
    errorMsg.classList.add('hidden');

    // 1. Отправляем email и password на сервер
    const response = await fetch('http://127.0.0.1:8000/auth/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
    });

    const data = await response.json();

    // 2. Если пароль или почта не подошли (статус 400 / 401 / 422)
    if (!response.ok) {
        errorMsg.innerText = data.detail || 'Неверный email или пароль';
        errorMsg.classList.remove('hidden');
        return;
    }

    // 3. Сохраняем полученный токен в память браузера
    localStorage.setItem('token', data.access_token);

    // 4. Расшифровываем среднюю часть токена, чтобы узнать роль (STUDENT или TEACHER)
    const payloadBase64 = data.access_token.split('.')[1].replace(/-/g, '+').replace(/_/g, '/');
    const payload = JSON.parse(atob(payloadBase64));

    if (payload.role === 'TEACHER') {
        window.location.href = 'html/dashboard.html'; // Укажи здесь имя файла преподавателя из папки html
    } else {
        window.location.href = 'index.html';
    }
});