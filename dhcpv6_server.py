import socket
from dhcpv6_message import DHCPv6Message

class DHCPv6Server:
    def __init__(self, interface, client_list):
        self.interface = interface
        self.sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        self.sock.bind(('::', 547))
        self.client_list = client_list

    def handle_request(self, data, addr):
        msg = DHCPv6Message.unpack(data)
        print(f"Received message type: {msg.msg_type} from {addr}")

        if msg.msg_type == 1:  # Solicit
            self.send_advertise(msg, addr)
            if addr[0] not in self.client_list:
                self.client_list.append(addr[0])

    def send_advertise(self, msg, addr):
        response_msg = DHCPv6Message(2, msg.transaction_id)
        response_data = response_msg.pack()
        self.sock.sendto(response_data, addr)
        print(f"Sent Advertise message to {addr}")

    def run(self):
        print("DHCPv6 Server is running")
        while True:
            data, addr = self.sock.recvfrom(1024)
            self.handle_request(data, addr)

def start_dhcpv6_server(client_list):
    server = DHCPv6Server(interface='eth0', client_list=client_list)
    server.run()