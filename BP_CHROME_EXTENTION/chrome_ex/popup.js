document.addEventListener('DOMContentLoaded', () => {
    const audio = document.getElementById('audio-btn');
    const saveLogsButton = document.getElementById("save-logs");
    let getJSONButton = document.getElementById('get-json');

    // Получаем сохраненное состояние из background.js
    chrome.runtime.sendMessage({ action: 'getRecordstate' }, (response) => {
        if (chrome.runtime.lastError) {
            console.error("Error getting audio state:", chrome.runtime.lastError);
            return;
        }

        audio.innerText = response?.isRecording === 'stop' ? 'Stop' : 'Start';
    });

    audio.addEventListener('click', () => {
        // Отправляем сообщение в background.js для переключения состояния
        chrome.runtime.sendMessage({ action: 'toggleRecord' }, (response) => {
            if (chrome.runtime.lastError) {
                console.error("Error toggling audio:", chrome.runtime.lastError);
                return;
            }

            audio.innerText = response?.isRecording === 'stop' ? 'Stop' : 'Start';
        });
    });

    
    // Добавляем обработчик клика
    saveLogsButton.addEventListener('click', function () {
        // Отправляем сообщение в content.js для сохранения логов
        chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
            chrome.tabs.sendMessage(tabs[0].id, { action: 'saveLogs' });
        });
    });

    getJSONButton.addEventListener('click', () => {
        fetch('http://127.0.0.1:5000/get_json', { method: 'GET' }) // Отправляем GET-запрос
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json(); // Получаем JSON-ответ
            })
            .then(data => {
                console.log('Data from server:', data);
                alert(`Received from server: ${JSON.stringify(data)}`); // Выводим полученные данные
            })
            .catch(error => {
                console.error('Error fetching data from server:', error);
            });
    });
 
});
