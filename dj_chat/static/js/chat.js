const chatId = document.querySelector('#message-form').getAttribute('data-chat-id');
const username = document.querySelector('#message-form').getAttribute('data-username');

var chatMessages = document.getElementById('chat-messages');
chatMessages.scrollTop = chatMessages.scrollHeight;

const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + chatId + '/'
);

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    console.log("Пришло сообщение от сервера, что сообщение создано");  // Проверьте вывод данных в консоль

    const messageElement = document.createElement('p');
    messageElement.innerHTML = `${data.message} <small>${new Date().toLocaleString()}</small>`;

    const chatMessages = document.querySelector('#chat-messages');
    chatMessages.appendChild(messageElement);

    // Ограничьте количество сообщений и прокрутите вниз
    const maxMessages = 50;  // Измените это на ваше предпочтение
    if (chatMessages.children.length > maxMessages) {
        chatMessages.removeChild(chatMessages.firstChild);
    }

    chatMessages.scrollTop = chatMessages.scrollHeight;
};


chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#message-form').onsubmit = function(e) {
    //console.log('Ваше сообщение отправлено на сервер: (' + message + ') имя пользователя:(' + username + ')')
    e.preventDefault();
    const messageInputDom = document.querySelector('#message-input');

    const message = messageInputDom.value;
    if(message === '')
        return;
    const username = document.querySelector('#message-form').getAttribute('data-username');

    chatSocket.send(JSON.stringify({
        'message': message,
        'room_name': chatId,
        'username': username
    }));

    messageInputDom.value = '';
};

function toggleModal(event) {
    var target = document.getElementById(event.currentTarget.dataset.target);
    target.open = !target.open;
  }

function createChat(event) {
    event.preventDefault();
    var chatName = document.getElementById('chat-name').value;
    var selectElement = document.getElementById('participants');
    var participants = Array.from(selectElement.selectedOptions).map(option => option.value);
  
    // Создаем объект с данными формы
    var data = {
        'name': chatName,
        'participants': participants
    };
  
    // Отправляем AJAX-запрос на сервер
    fetch('/chats/create_chat/', {  // замените '/create_chat/' на URL вашего endpoint
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        // Вставьте здесь CSRF-токен, если он вам нужен
      },
      body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
      // Обрабатываем ответ сервера здесь
      console.log(data);
      // Закрываем модальное окно
      var target = document.getElementById(event.currentTarget.dataset.target);
      target.open = !target.open;
      // Перезагружаем страницу
      location.reload();

    })
    .catch((error) => {
      console.error('Error:', error);
      location.reload();
    });
    location.reload();
}


  
