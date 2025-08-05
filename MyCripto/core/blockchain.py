import os
import time
import json

from utils.crypto_utils import sha256
from core.transaction import Transaction
from config import settings


class Block:
    def __init__(self, index, transactions, previous_hash, nonce=0, timestamp=None, hash=None):
        self.index = index
        self.transactions = transactions  # lista Transaction objekata
        self.previous_hash = previous_hash
        self.timestamp = timestamp or time.time()
        self.nonce = nonce
        self.hash = hash or self.calculate_hash()

    def calculate_hash(self):
        data = json.dumps({
            "index": self.index,
            "transactions": [tx.to_dict() for tx in self.transactions],
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "nonce": self.nonce
        }, sort_keys=True)
        return sha256(data)

    def mine(self, difficulty):
        """
        Proof-of-Work mining:
        Povećava nonce dok hash ne počinje sa zadatim brojem nula (difficulty)
        """
        print("⛏️ Početak rudarenja bloka...")
        start = time.time()
        while not self.hash.startswith("0" * difficulty):
            self.nonce += 1
            self.hash = self.calculate_hash()
            # Opcionalno: možeš dodati print svakih X iteracija da vidiš napredak (za testiranje)
        end = time.time()
        print(f"✅ Blok izrudaren u {end - start:.2f} sekundi. Hash: {self.hash}")


class Blockchain:
    def __init__(self):
        self.chain = []
        self.load_chain()

    def load_chain(self):
        if not os.path.exists(settings.BLOCKCHAIN_FILE):
            print("Blockchain fajl ne postoji, kreiram genesis blok.")
            self.create_genesis_block()
            self.save_chain()
            return

        with open(settings.BLOCKCHAIN_FILE, "r") as f:
            content = f.read().strip()
            if not content:
                print("Blockchain fajl prazan, kreiram genesis blok.")
                self.create_genesis_block()
                self.save_chain()
                return

            data = json.loads(content)
            self.chain = [
                Block(
                    index=block["index"],
                    transactions=[Transaction(**tx) for tx in block["transactions"]],
                    previous_hash=block["previous_hash"],
                    nonce=block["nonce"],
                    timestamp=block["timestamp"],
                    hash=block["hash"]
                )
                for block in data
            ]

    def create_genesis_block(self):
        genesis = Block(0, [], "0")
        self.chain.append(genesis)

    def save_chain(self):
        os.makedirs(os.path.dirname(settings.BLOCKCHAIN_FILE), exist_ok=True)
        with open(settings.BLOCKCHAIN_FILE, "w") as f:
            json.dump([{
                "index": block.index,
                "transactions": [tx.to_dict() for tx in block.transactions],
                "previous_hash": block.previous_hash,
                "timestamp": block.timestamp,
                "nonce": block.nonce,
                "hash": block.hash
            } for block in self.chain], f, indent=4)

    def get_last_block(self):
        return self.chain[-1]

    def add_block(self, transactions):
        last_block = self.get_last_block()
        new_block = Block(
            index=last_block.index + 1,
            transactions=transactions,
            previous_hash=last_block.hash
        )
        new_block.mine(settings.DIFFICULTY)
        self.chain.append(new_block)
        self.save_chain()

    def get_balance(self, address: str) -> float:
        balance = 0.0
        for block in self.chain:
            for tx in block.transactions:
                if tx.recipient == address:
                    balance += tx.amount
                if tx.sender == address:
                    balance -= tx.amount
        return balance

    def mine_pending_transactions(self, miner_address, pending_transactions):
        """
        Rudari blok sa svim pending transakcijama i dodeljuje mining reward mineru.
        """
        print(f"⛏️ {miner_address} započinje rudarenje...")

        # Simuliraj vreme rudarenja (može se izostaviti jer pravi mining traje)
        for i in range(5):
            print(f"⛏️ Rudarenje... {i + 1}/5 sekundi")
            time.sleep(1)

        # Dodaj nagradnu transakciju mineru
        reward_tx = Transaction(sender="MINING_REWARD", recipient=miner_address, amount=settings.MINING_REWARD)
        all_transactions = pending_transactions + [reward_tx]

        # Dodaj novi blok sa transakcijama
        self.add_block(all_transactions)

        print(f"🎉 {miner_address} je uspešno izrudario blok i dobio {settings.MINING_REWARD} MB!")
