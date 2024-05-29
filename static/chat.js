document.addEventListener('DOMContentLoaded', (event) => {
    var socket = io();

    socket.on('update_clients', function(clients) {
        var clientsList = document.getElementById("clients");
        clientsList.innerHTML = '';
        clients.forEach(function(client) {
            var li = document.createElement("li");
            li.appendChild(document.createTextNode(client));
            clientsList.appendChild(li);
        });
    });

    socket.on('message', function(msg) {
        var li = document.createElement("li");
        li.appendChild(document.createTextNode(msg));
        document.getElementById("messages").appendChild(li);
    });
});

function sendMessage() {
    var input = document.getElementById("message");
    var message = input.value;
    input.value = '';
    var socket = io();
    socket.send(message);
}