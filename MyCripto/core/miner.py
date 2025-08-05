import time
from core.transaction import Transaction
from core.blockchain import Blockchain
from core.blockchain import Blockchain, Block

from core.mempool import Mempool
from config import settings

class Miner:
    def __init__(self, miner_address):
        self.miner_address = miner_address
        self.blockchain = Blockchain()
        self.mempool = Mempool()

    def mine_pending_transactions(self):
        pending_tx_dicts = self.mempool.get_transactions()

        if not pending_tx_dicts:
            print("No transactions to mine.")
            return None

        # Pretvori transakcije iz dict u Transaction objekte
        pending_txs = []
        for tx_dict in pending_tx_dicts:
            tx = Transaction(
                sender=tx_dict["sender"],
                recipient=tx_dict["recipient"],
                amount=tx_dict["amount"],
                timestamp=tx_dict["timestamp"],
                signature=tx_dict["signature"]
            )
            if not tx.is_valid():
                print("Invalid transaction found in mempool, skipping.")
                continue
            pending_txs.append(tx)

        # Dodaj nagradu za rudara kao posebnu transakciju sa sender="MINING_REWARD"
        reward_tx = Transaction(
            sender="MINING_REWARD",
            recipient=self.miner_address,
            amount=settings.MINING_REWARD,
            timestamp=time.time(),
            signature=""  # ne treba potpis za nagradu
        )

        pending_txs.append(reward_tx)

        # Dodaj novi blok sa transakcijama u blockchain
        self.blockchain.add_block(pending_txs)

        # Ukloni rudirane transakcije iz mempool-a (osim nagrade)
        self.mempool.clear_transactions(pending_tx_dicts)

        return self.blockchain.get_last_block().hash

    def mine_with_time_limit(self, duration_seconds: int):
        """
        Mine solving hash puzzle with nonce increments for a limited duration.
        """
        last_block = self.blockchain.get_last_block()
        transactions = []

        # Uzmi transakcije iz mempoola ako ih ima
        pending_tx_dicts = self.mempool.get_transactions()
        for tx_dict in pending_tx_dicts:
            tx = Transaction(
                sender=tx_dict["sender"],
                recipient=tx_dict["recipient"],
                amount=tx_dict["amount"],
                timestamp=tx_dict["timestamp"],
                signature=tx_dict["signature"]
            )
            if tx.is_valid():
                transactions.append(tx)

        # Dodaj nagradnu transakciju rudaru
        reward_tx = Transaction(
            sender="MINING_REWARD",
            recipient=self.miner_address,
            amount=settings.MINING_REWARD,
            timestamp=time.time(),
            signature=""
        )
        transactions.append(reward_tx)

        new_block = self.blockchain.get_last_block()
        index = new_block.index + 1
        previous_hash = new_block.hash

        block = self.blockchain.chain[-1]
        # Kreiraj novi blok koji ćemo minerovati
        new_block = self.blockchain.chain[-1]
        new_block = self.blockchain.get_last_block()
        block_to_mine = Block(index=index, transactions=transactions, previous_hash=previous_hash)

        start_time = time.time()
        nonce = 0
        difficulty = settings.DIFFICULTY
        target = "0" * difficulty

        while time.time() - start_time < duration_seconds:
            block_to_mine.nonce = nonce
            block_to_mine.hash = block_to_mine.calculate_hash()
            if block_to_mine.hash.startswith(target):
                print(f"✅ Valid nonce found: {nonce} with hash {block_to_mine.hash}")
                self.blockchain.chain.append(block_to_mine)
                self.blockchain.save_chain()
                # Očisti rudirane transakcije iz mempoola
                self.mempool.clear_transactions(pending_tx_dicts)
                return block_to_mine.hash
            nonce += 1

        # Nije pronađen validan nonce u datom vremenu
        return None
