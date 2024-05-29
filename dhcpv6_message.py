import struct

class DHCPv6Message:
    def __init__(self, msg_type, transaction_id, options=None):
        self.msg_type = msg_type
        self.transaction_id = transaction_id
        self.options = options if options else []

    def pack(self):
        # Empaquetar mensaje DHCPv6 (simplificado)
        packed_data = struct.pack('!B', self.msg_type)
        packed_data += struct.pack('!I', self.transaction_id)[1:]  # Usar sólo 3 bytes
        for option in self.options:
            packed_data += option.pack()
        return packed_data

    @staticmethod
    def unpack(data):
        # Desempaquetar mensaje DHCPv6 (simplificado)
        msg_type = struct.unpack('!B', data[:1])[0]
        transaction_id = struct.unpack('!I', b'\x00' + data[1:4])[0]
        # Omitir opciones por simplicidad
        return DHCPv6Message(msg_type, transaction_id)
