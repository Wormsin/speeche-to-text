function formatDate(date) {
  let year = date.getFullYear();
  let month = (date.getMonth() + 1).toString().padStart(2, '0');
  let day = date.getDate().toString().padStart(2, '0');
  let hours = date.getHours().toString().padStart(2, '0');
  let minutes = date.getMinutes().toString().padStart(2, '0');
  let seconds = date.getSeconds().toString().padStart(2, '0');

  return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
}

let logs = [];

// Обработчик кликов на элементы
document.addEventListener('click', function (event) {
    let clickedElement = event.target;
    let timestamp = formatDate(new Date());
    let logEntry = `[${timestamp}] Клик по элементу: ${clickedElement.outerHTML}`;
    logs.push(logEntry);
    console.log(logEntry);
});

// Получаем сообщение из popup и запускаем сохранение логов
chrome.runtime.onMessage.addListener(function (message, sender, sendResponse) {
    if (message.action === 'saveLogs') {
        // Отправляем логи в background для сохранения
        chrome.runtime.sendMessage({ action: 'saveLogs', logs: logs });
        logs = []; // Очищаем логи после отправки
    }
});
