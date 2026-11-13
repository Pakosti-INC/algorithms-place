const TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzIiwicm9sZSI6IlNUVURFTlQiLCJncm91cF9pZCI6MSwiZXhwIjoxNzk0NjcwMzcwfQ.RMJHyHEhWDOyJaXowO2CHeL3xwbKEtis6e_BAQEefYQ';

//функция полученния данных
async function getData() {
    const response = await fetch('http://127.0.0.1:8000/problems', {
        headers: {
            'Authorization': `Bearer ${TOKEN}`
        }   
    });
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
        input_code: userCode,
        problem_id: 1,
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