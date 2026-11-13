//функция полученния данных
async function getData() {
    const response = await fetch('http://127.0.0.1:8000/problems');
    
    // 2. Распаковывка ответа из JSON в обычный JS-объект/массив
    const data = await response.json();
    
    // 3. Делаем что-то с данными (выводим в консоль или в HTML)
    console.log(data);
}


//функция отправки данных
async function sendData() {
    // 1. Собираем объект с нужными полями (как ждёт бэкенд)
    const userCode = document.getElementById('code-editor').innerText;
    
    const payload = {
        input_code: '...',
        problem_id: 1,
        notes: null 
    };

    // 2. Отправляем запрос с настройками
    const response = await fetch('http://127.0.0.1:8000/submissions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload) // превращаем объект в текст
    });

    // 3. Читаем ответ сервера
    const result = await response.json();
    console.log(result);
}

getData();
document.getElementById('submit-btn').addEventListener('click', sendData);