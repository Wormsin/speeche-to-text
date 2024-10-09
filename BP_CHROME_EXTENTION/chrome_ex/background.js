let isRecording = 'start'; // Начальное состояние кнопки


// Обработка сообщений из popup.js
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'getRecordstate') {
        // Отправка текущего состояния кнопки
        sendResponse({ isRecording: isRecording });
    } else if (request.action === 'toggleRecord') {
        // Переключение состояния кнопки
        const previousState = isRecording;
        isRecording = isRecording === 'start' ? 'stop' : 'start';

        // Отправка состояния кнопки на сервер
        if (previousState === 'start' && isRecording === 'stop') {
            sendRecordStateToServer('/start')
                .then(() => {
                    sendResponse({ isRecording: isRecording });
                })
                .catch((error) => {
                    console.error('Error sending state to server:', error);
                    sendResponse({ error: 'Failed to send state to server' });
                });
        } else if (previousState === 'stop' && isRecording === 'start') {
            sendRecordStateToServer('/stop')
                .then(() => {
                    sendResponse({ isRecording: isRecording });
                })
                .catch((error) => {
                    console.error('Error sending state to server:', error);
                    sendResponse({ error: 'Failed to send state to server' });
                });
        }

        return true; // Указывает, что ответ будет отправлен асинхронно

    } else if (request.action === 'saveLogs') {
        let logs = request.logs;

        // Создаем Blob из накопленных логов
        let blob = new Blob([logs.join('\n')], { type: 'text/plain' });

        // Преобразуем Blob в Base64
        let reader = new FileReader();
        reader.onloadend = function () {
            let base64data = reader.result.split(',')[1]; // получаем только часть данных base64

            // Используем chrome.downloads для загрузки файла напрямую
            chrome.downloads.download({
                url: 'data:text/plain;base64,' + base64data,
                filename: 'BP_logs/logs.txt',
                saveAs: true
            }, function (downloadId) {
                if (downloadId) {
                    console.log("Файл успешно сохранён");
                } else {
                    console.error("Ошибка при сохранении файла");
                }
            });
        };
        reader.readAsDataURL(blob); // Чтение Blob как Data URL
    } else {
        sendResponse({ error: 'Unknown action' });
    }
});

// Функция для отправки состояния кнопки на сервер
async function sendRecordStateToServer(endpoint) {
    const response = await fetch(`http://127.0.0.1:5000${endpoint}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ state: endpoint === '/start' ? 'start' : 'stop' }),
    });

    if (!response.ok) {
        throw new Error('Network response was not ok: ' + response.statusText);
    }
}