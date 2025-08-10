import time
from core.transaction import Transaction
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

        reward_tx = Transaction(
            sender="MINING_REWARD",
            recipient=self.miner_address,
            amount=settings.MINING_REWARD,
            timestamp=time.time(),
            signature=""
        )

        pending_txs.append(reward_tx)

        self.blockchain.add_block(pending_txs)

        self.mempool.clear_transactions(pending_tx_dicts)

        return self.blockchain.get_last_block().hash

    def mine_with_time_limit(self, duration_seconds: int):
        last_block = self.blockchain.get_last_block()
        transactions = []

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

        reward_tx = Transaction(
            sender="MINING_REWARD",
            recipient=self.miner_address,
            amount=settings.MINING_REWARD,
            timestamp=time.time(),
            signature=""
        )
        transactions.append(reward_tx)

        index = last_block.index + 1
        previous_hash = last_block.hash

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
                self.mempool.clear_transactions(pending_tx_dicts)
                return block_to_mine.hash
            nonce += 1

        return None

    def auto_mine(self):
        difficulty = settings.DIFFICULTY
        target = "0" * difficulty
        mined_count = 0

        while True:
            last_block = self.blockchain.get_last_block()
            pending_tx_dicts = self.mempool.get_transactions()
            transactions = []

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

            reward_tx = Transaction(
                sender="MINING_REWARD",
                recipient=self.miner_address,
                amount=settings.MINING_REWARD,
                timestamp=time.time(),
                signature=""
            )
            transactions.append(reward_tx)

            index = last_block.index + 1
            previous_hash = last_block.hash
            block_to_mine = Block(index=index, transactions=transactions, previous_hash=previous_hash)

            nonce = 0
            start_time = time.time()

            print(f"\n⛏️ Starting mining for block #{index} ... Difficulty: {difficulty}")
            while True:
                block_to_mine.nonce = nonce
                block_to_mine.hash = block_to_mine.calculate_hash()

                if block_to_mine.hash.startswith(target):
                    self.blockchain.chain.append(block_to_mine)
                    self.blockchain.save_chain()
                    self.mempool.clear_transactions(pending_tx_dicts)
                    mined_count += 1
                    elapsed = time.time() - start_time
                    print(f"✅ Block #{index} mined! Hash: {block_to_mine.hash} | Time: {elapsed:.2f}s | Total mined: {mined_count}")
                    break

                if nonce % 100000 == 0:
                    print(f"🔄 Nonce tried: {nonce}")

                nonce += 1

