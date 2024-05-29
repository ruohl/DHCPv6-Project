from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit
import threading
from dhcpv6_server import start_dhcpv6_server

app = Flask(__name__)
socketio = SocketIO(app)

# Lista compartida entre los clientes conectados
connected_clients = []

@app.route('/')
def index():
    return render_template('index.html', clients=connected_clients)

@socketio.on('connect')
def handle_connect():
    client_ip = request.remote_addr
    if client_ip not in connected_clients:
        connected_clients.append(client_ip)
    emit('update_clients', connected_clients, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    client_ip = request.remote_addr
    if client_ip in connected_clients:
        connected_clients.remove(client_ip)
    emit('update_clients', connected_clients, broadcast=True)

@socketio.on('message')
def handle_message(msg):
    print(f"Message: {msg}")
    send(msg, broadcast=True)

if __name__ == "__main__":
    dhcp_thread = threading.Thread(target=start_dhcpv6_server, args=(connected_clients,))
    dhcp_thread.start()
    socketio.run(app, host='0.0.0.0', port=5000)
