from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit
import threading
from dhcpv6_server import start_dhcpv6_server

app = Flask(__name__)
socketio = SocketIO(app)

# Diccionario compartido entre los clientes conectados, con IP como clave
connected_clients = {}

@app.route('/')
def index():
    return render_template('index.html', clients=connected_clients.values())

@socketio.on('connect')
def handle_connect():
    client_ip = request.remote_addr
    if client_ip not in connected_clients:
        connected_clients[client_ip] = {'ip': client_ip, 'username': 'Anonymous'}
    emit('update_clients', list(connected_clients.values()), broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    client_ip = request.remote_addr
    if client_ip in connected_clients:
        del connected_clients[client_ip]
    emit('update_clients', list(connected_clients.values()), broadcast=True)

@socketio.on('message')
def handle_message(msg):
    client_ip = request.remote_addr
    if client_ip in connected_clients:
        connected_clients[client_ip]['username'] = msg['username']
    send(msg, broadcast=True)
    emit('update_clients', list(connected_clients.values()), broadcast=True)

if __name__ == "__main__":
    dhcp_thread = threading.Thread(target=start_dhcpv6_server, args=(connected_clients,))
    dhcp_thread.start()
    socketio.run(app, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)