# web_server.py
from flask import Flask, render_template
from flask_socketio import SocketIO, send
import threading
from dhcpv6_server import start_dhcpv6_server

app = Flask(__name__)
socketio = SocketIO(app)

# Lista compartida entre el servidor DHCPv6 y el servidor web
client_list = []

@app.route('/')
def index():
    return render_template('index.html', clients=client_list)

@socketio.on('message')
def handle_message(msg):
    print(f"Message: {msg}")
    send(msg, broadcast=True)

def start_web_server():
    socketio.run(app, host='0.0.0.0', port=5000)

if __name__ == "__main__":
    # Iniciar servidor DHCPv6 en un hilo separado
    dhcp_thread = threading.Thread(target=start_dhcpv6_server, args=(client_list,))
    dhcp_thread.start()

    # Iniciar servidor web
    start_web_server()
