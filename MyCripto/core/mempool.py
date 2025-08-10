import os
import json
from config import settings

MEMPOOL_FILE = "data/mempool.json"

class Mempool:
    def __init__(self):
        self.transactions = []
        self.load()

    def load(self):
        if not os.path.exists(MEMPOOL_FILE):
            self.transactions = []
            self.save()
            return

        with open(MEMPOOL_FILE, "r") as f:
            content = f.read().strip()
            if not content:
                self.transactions = []
                self.save()
                return

            self.transactions = json.loads(content)

    def save(self):
        os.makedirs(os.path.dirname(MEMPOOL_FILE), exist_ok=True)
        with open(MEMPOOL_FILE, "w") as f:
            json.dump(self.transactions, f, indent=4)

    def add_transaction(self, tx_dict):
        self.transactions.append(tx_dict)
        self.save()

    def clear_transactions(self, txs_to_remove):
        self.transactions = [
            tx for tx in self.transactions if tx not in txs_to_remove
        ]
        self.save()

    def get_transactions(self):
        return self.transactions

    def has_transaction(self, tx_dict) -> bool:
        """
        Proverava da li data transakcija (tx_dict) već postoji u mempoolu.
        Upoređuje po potpisu (signature) koji bi trebalo da bude jedinstven.
        """
        tx_signature = tx_dict.get("signature")
        if not tx_signature:
            return False

        for tx in self.transactions:
            if tx.get("signature") == tx_signature:
                return True
        return False

