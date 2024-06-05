document.addEventListener('DOMContentLoaded', (event) => {
    var socket = io();

    socket.on('update_clients', function(clients) {
        var clientsList = document.getElementById("clients");
        clientsList.innerHTML = '';
        clients.forEach(function(client) {
            var li = document.createElement("li");
            li.appendChild(document.createTextNode(client.username || 'Anonymous'));
            clientsList.appendChild(li);
        });
    });

    socket.on('message', function(msg) {
        var li = document.createElement("li");
        li.appendChild(document.createTextNode(`${msg.username}: ${msg.text}`));
        document.getElementById("messages").appendChild(li);
    });
});

function mandarMensaje() {
    var usernameInput = document.getElementById("username");
    var messageInput = document.getElementById("message");
    var username = usernameInput.value || 'Anonymous';
    var message = messageInput.value;
    messageInput.value = '';
    var socket = io();
    socket.emit('message', { username: username, text: message });
    document.getElementById("username").innerText = username;
    if (username !== 'Anonymous') {
        usernameInput.disabled = true;
    }
}