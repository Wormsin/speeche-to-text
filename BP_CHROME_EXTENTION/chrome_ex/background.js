//chrome.runtime.onInstalled.addListener(() => {
//    console.log('Extension installed and ready to log interactions.');
//});

chrome.runtime.onMessage.addListener(function (message, sender, sendResponse) {
    if (message.action === 'saveLogs') {
        let logs = message.logs;

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
    }
});



