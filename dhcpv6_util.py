# dhcpv6_util.py
def generate_transaction_id():
    import random
    return random.randint(0, 0xFFFFFF)