const chatId = document.querySelector('#message-form').getAttribute('data-chat-id');
const username = document.querySelector('#message-form').getAttribute('data-username');

const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + chatId + '/'  // добавьте chatId в конец URL
);


// Остальной код без изменений
chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);

    

    const messageElement = document.createElement('p');
    messageElement.innerHTML = `${data.message} <small>${new Date().toLocaleString()}</small>`;
    console.log(username)
    if (data.chat_id === chatId) {
        
    }
    document.querySelector('#chat-messages').appendChild(messageElement);

};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#message-form').onsubmit = function(e) {
    e.preventDefault();
    const messageInputDom = document.querySelector('#message-input');
    const message = messageInputDom.value;

    const username = document.querySelector('#message-form').getAttribute('data-username');
    console.log(username);
    chatSocket.send(JSON.stringify({
        'message': message,
        'chat_id': chatId,
        'username': username
    }));

    messageInputDom.value = '';
};
