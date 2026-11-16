document.addEventListener('DOMContentLoaded', () => {
    // 1. Логика аккордеонов разделов
    document.querySelectorAll('.accordion-btn').forEach((button) => {
        button.addEventListener('click', () => {
            const content = button.nextElementSibling;
            const icon = button.querySelector('.icon-rotate');

            if (content) content.classList.toggle('hidden');
            if (icon) icon.classList.toggle('rotate-180');
        });
    });

    // 2. Кнопка выхода
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', () => {
            localStorage.removeItem('token');
            window.location.href = 'login.html';
        });
    }

    // 3. Загрузка задач с бэкенда (/problems)
    loadDashboardData();
});

async function loadDashboardData() {
    const token = localStorage.getItem('token');
    const container = document.getElementById('problems-container');
    if (!token || !container) return;

    try {
        const response = await fetch('http://127.0.0.1:8000/problems', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (!response.ok) return;

        const problems = await response.json();
        if (!Array.isArray(problems) || problems.length === 0) return;

        container.innerHTML = '';
        problems.forEach((problem) => {
            const row = document.createElement('div');
            row.className = 'task-row';
            row.innerHTML = `
                <div class="task-row-left">
                    <span class="status-badge status-default">Не начато</span>
                    <span class="task-row-title">${problem.id}. ${problem.title}</span>
                </div>
                <div class="task-row-actions">
                    <span class="task-difficulty">${problem.difficulty || ''}</span>
                    <a href="task.html?id=${problem.id}" class="link-solve">Решить →</a>
                </div>
            `;
            container.appendChild(row);
        });
    } catch (err) {
        console.error('Не удалось загрузить список задач:', err);
    }
}