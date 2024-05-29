document.addEventListener('DOMContentLoaded', (event) => {
    var socket = io();

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