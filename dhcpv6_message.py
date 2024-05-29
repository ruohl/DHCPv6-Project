class DHCPv6Message:
    def __init__(self, msg_type, transaction_id):
        self.msg_type = msg_type
        self.transaction_id = transaction_id

    def pack(self):
        return self.msg_type.to_bytes(1, 'big') + self.transaction_id.to_bytes(3, 'big')

    @classmethod
    def unpack(cls, data):
        msg_type = data[0]
        transaction_id = int.from_bytes(data[1:4], 'big')
        return cls(msg_type, transaction_id)