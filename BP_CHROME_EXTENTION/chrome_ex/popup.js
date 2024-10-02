document.addEventListener('DOMContentLoaded', function () {
    // Находим кнопку
    let saveLogsButton = document.getElementById('save-logs');
    let runPythonButton = document.getElementById('run-python');
    
    // Добавляем обработчик клика
    saveLogsButton.addEventListener('click', function () {
        // Отправляем сообщение в content.js для сохранения логов
        chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
            chrome.tabs.sendMessage(tabs[0].id, { action: 'saveLogs' });
        });
    });


    runPythonButton.addEventListener('click', function () {
        fetch('http://localhost:8000', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: 'Запуск Python-кода из расширения' })
        })
            .then(response => response.json())
            .then(data => {
                console.log('Ответ от сервера:', data);
            })
            .catch(error => {
                console.error('Ошибка:', error);
            });
    });

});
