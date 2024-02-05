const chatId = document.querySelector('#message-form').getAttribute('data-chat-id');
const username = document.querySelector('#message-form').getAttribute('data-username');

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

    if (data.room_name === chatId) {
        document.querySelector('#chat-messages').appendChild(messageElement);
    }
};


chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#message-form').onsubmit = function(e) {
    e.preventDefault();
    const messageInputDom = document.querySelector('#message-input');
    const message = messageInputDom.value;

    const username = document.querySelector('#message-form').getAttribute('data-username');

    chatSocket.send(JSON.stringify({
        'message': message,
        'room_name': chatId,
        'username': username
    }));

    messageInputDom.value = '';
};

