const TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzIiwicm9sZSI6IlNUVURFTlQiLCJncm91cF9pZCI6MSwiZXhwIjoxNzk0OTE3NjczfQ.11xPZz2Ydsb9g3wOgO9HNQQ0Je76sNCi-jYWd7rFwXo';
let currentProblemId = 1;


function renderProblemDetails(problem) {
    currentProblemId = problem.id;

    const difficulty = problem.difficulty ? ` / ${problem.difficulty}` : '';
    document.getElementById('problem-badge').innerText = `ЗАДАЧА #${problem.id}${difficulty}`;
    document.getElementById('problem-title').innerText = problem.title;
    document.getElementById('problem-description').innerHTML = `<p>${problem.description}</p>`;
}


//функция полученния данных
async function getData() {
    const response = await fetch('http://127.0.0.1:8000/problems', {
        headers: {
            'Authorization': `Bearer ${TOKEN}`
        }   
    });
    // 2. Распаковывка ответа из JSON в обычный JS-объект/массив
    const data = await response.json();
    
    const listContainer = document.getElementById('problems-list');
    listContainer.innerHTML = ''; // Очищаем статичные заглушки
    
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

        // При клике на задачу открываем её условие по центру
        btn.addEventListener('click', () => renderProblemDetails(problem));
        listContainer.appendChild(btn);

        // Первую задачу из списка открываем автоматически при загрузке
        if (index === 0) {
            renderProblemDetails(problem);
        }
    });
    // 3. Делаем что-то с данными (выводим в консоль или в HTML)
    console.log(data);
}


//функция отправки данных
async function sendData() {
    // 1. Собираем объект с нужными полями (как ждёт бэкенд)
    const userCode = document.getElementById('code-editor').innerText;
    
    const payload = {
        input_code: userCode,
        problem_id: currentProblemId,
        notes: null 
    };

    // 2. Отправляем запрос с настройками
    const response = await fetch('http://127.0.0.1:8000/submissions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json',
                'Authorization': `Bearer ${TOKEN}`},
        body: JSON.stringify(payload) // превращаем объект в текст
        
        
    });

    // 3. Читаем ответ сервера
    const result = await response.json();
    console.log(result);
}

getData();
document.getElementById('submit-btn').addEventListener('click', sendData);