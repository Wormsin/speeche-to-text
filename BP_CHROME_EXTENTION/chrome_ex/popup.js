document.addEventListener('DOMContentLoaded', function () {
    // Находим кнопку
    let saveLogsButton = document.getElementById('save-logs');

    // Добавляем обработчик клика
    saveLogsButton.addEventListener('click', function () {
        // Отправляем сообщение в content.js для сохранения логов
        chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
            chrome.tabs.sendMessage(tabs[0].id, { action: 'saveLogs' });
        });
    });
});
