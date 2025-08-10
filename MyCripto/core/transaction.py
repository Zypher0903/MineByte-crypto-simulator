from utils.crypto_utils import sign_message, verify_signature
import time

class Transaction:
    def __init__(self, sender, recipient, amount, signature=None, timestamp=None):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.timestamp = timestamp or time.time()
        self.signature = signature

    def to_dict(self, include_signature=True):
        tx = {
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "timestamp": self.timestamp
        }
        if include_signature and self.signature:
            tx["signature"] = self.signature
        return tx

    def get_message(self):
        return f"{self.sender}{self.recipient}{self.amount}{self.timestamp}"

    def sign(self, private_key):
        self.signature = sign_message(private_key, self.get_message())

    def is_valid(self):
        if self.sender == "SYSTEM":
            return True  # rudarska nagrada
        if not self.signature:
            return False
        return verify_signature(self.sender, self.get_message(), self.signature)


