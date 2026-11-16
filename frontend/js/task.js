const FALLBACK_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzIiwicm9sZSI6IlNUVURFTlQiLCJncm91cF9pZCI6MSwiZXhwIjoxNzk0OTE3NjczfQ.11xPZz2Ydsb9g3wOgO9HNQQ0Je76sNCi-jYWd7rFwXo';
let currentProblemId = 1;

function getAuthToken() {
    return localStorage.getItem('token') || FALLBACK_TOKEN;
}

document.addEventListener('DOMContentLoaded', () => {
    initPanelsToggle();
    initLineNumbers();
    getData();

    const submitBtn = document.getElementById('submit-btn');
    if (submitBtn) {
        submitBtn.addEventListener('click', sendData);
    }
});

// 1. Работа стрелочек сворачивания панелей
function initPanelsToggle() {
    const leftPanel = document.getElementById('left-panel');
    const toggleLeftBtn = document.getElementById('toggle-left');

    const middlePanel = document.getElementById('middle-panel');
    const toggleMiddleBtn = document.getElementById('toggle-middle');
    const rightPanel = document.getElementById('right-panel');

    if (toggleLeftBtn && leftPanel) {
        toggleLeftBtn.addEventListener('click', () => {
            leftPanel.classList.toggle('is-collapsed');
            toggleLeftBtn.classList.toggle('collapsed');
        });
    }

    if (toggleMiddleBtn && middlePanel && rightPanel) {
        toggleMiddleBtn.addEventListener('click', () => {
            const collapsed = middlePanel.classList.toggle('is-collapsed');
            toggleMiddleBtn.classList.toggle('collapsed');
            rightPanel.classList.toggle('is-expanded', collapsed);
        });
    }
}

// 2. Автоматическая нумерация строк в редакторе
function initLineNumbers() {
    const editor = document.getElementById('code-editor');
    const lineNumbers = document.getElementById('line-numbers');
    if (!editor || !lineNumbers) return;

    const updateNumbers = () => {
        // Считаем реальное число строк по символу переноса (учитываем поведение contenteditable)
        const text = editor.innerText.replace(/\n$/, '');
        const lineCount = text === '' ? 1 : text.split('\n').length;

        lineNumbers.innerHTML = Array.from(
            { length: lineCount },
            (_, i) => `<div>${i + 1}</div>`
        ).join('');
    };

    editor.addEventListener('input', updateNumbers);
    updateNumbers();
}

// 3. Отрисовка условия выбранной задачи
function renderProblemDetails(problem) {
    currentProblemId = problem.id;

    const difficulty = problem.difficulty ? ` / ${problem.difficulty}` : '';
    document.getElementById('problem-badge').innerText = `ЗАДАЧА #${problem.id}${difficulty}`;
    document.getElementById('problem-title').innerText = problem.title;
    document.getElementById('problem-description').innerHTML = `<p>${problem.description}</p>`;
}

// 4. Получение списка задач с сервера
async function getData() {
    try {
        const response = await fetch('http://127.0.0.1:8000/problems', {
            headers: {
                'Authorization': `Bearer ${getAuthToken()}`
            }
        });
        const data = await response.json();

        const listContainer = document.getElementById('problems-list');
        listContainer.innerHTML = '';

        data.forEach((problem, index) => {
            const btn = document.createElement('button');
            btn.className = 'flex items-center justify-between px-6 py-4 hover:bg-slate-50 border-b border-slate-100 transition text-left w-full';
            btn.innerHTML = `
                <div class="flex items-center gap-3">
                    <div class="w-4 h-4 rounded-full border-2 border-slate-300 flex-shrink-0"></div>
                    <span class="text-sm font-medium text-slate-700">${problem.id}. ${problem.title}</span>
                </div>
                <span class="text-xs font-mono text-slate-400">${problem.difficulty || ''}</span>
            `;

            btn.addEventListener('click', () => renderProblemDetails(problem));
            listContainer.appendChild(btn);

            if (index === 0) {
                renderProblemDetails(problem);
            }
        });
    } catch (err) {
        console.error('Ошибка загрузки задач:', err);
    }
}

// 5. Отправка решения на проверку
async function sendData() {
    const userCode = document.getElementById('code-editor').innerText;

    const payload = {
        input_code: userCode,
        problem_id: currentProblemId,
        notes: null
    };

    const response = await fetch('http://127.0.0.1:8000/submissions', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${getAuthToken()}`
        },
        body: JSON.stringify(payload)
    });

    const result = await response.json();
    console.log(result);
}