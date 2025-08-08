from flask import Flask, request, jsonify
from core.blockchain import Blockchain
from core.transaction import Transaction
from core.mempool import Mempool
from core.wallet import Wallet
from core.miner import Miner
import threading
import requests
import time

app = Flask(__name__)

blockchain = Blockchain()
mempool = Mempool()
peers = set()

# ----------------- API Endpoints -----------------

@app.route('/blockchain', methods=['GET'])
def get_blockchain():
    chain_data = [{
        "index": block.index,
        "transactions": [tx.to_dict() for tx in block.transactions],
        "previous_hash": block.previous_hash,
        "timestamp": block.timestamp,
        "nonce": block.nonce,
        "hash": block.hash
    } for block in blockchain.chain]
    return jsonify({"length": len(chain_data), "chain": chain_data})


@app.route('/mempool', methods=['GET'])
def get_mempool():
    return jsonify(mempool.get_transactions())


@app.route('/transaction', methods=['POST'])
def add_transaction():
    tx_data = request.get_json()
    try:
        tx = Transaction(
            sender=tx_data['sender'],
            recipient=tx_data['recipient'],
            amount=tx_data['amount'],
            timestamp=tx_data.get('timestamp', None),
            signature=tx_data['signature']
        )
        if not tx.is_valid():
            return jsonify({"message": "Invalid transaction signature"}), 400

        if mempool.has_transaction(tx.to_dict()):
            return jsonify({"message": "Transaction already in mempool"}), 409

        mempool.add_transaction(tx.to_dict())
        broadcast_transaction(tx.to_dict())

        return jsonify({"message": "Transaction added to mempool"}), 201
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 400


@app.route('/block', methods=['POST'])
def add_block():
    block_data = request.get_json()
    try:
        transactions = [Transaction(**tx) for tx in block_data['transactions']]
        new_block = blockchain.chain[-1].__class__(
            index=block_data['index'],
            transactions=transactions,
            previous_hash=block_data['previous_hash'],
            nonce=block_data['nonce'],
            timestamp=block_data['timestamp'],
            hash=block_data['hash']
        )
        # Validacija bloka:
        last_block = blockchain.get_last_block()
        if new_block.previous_hash != last_block.hash:
            return jsonify({"message": "Previous hash does not match"}), 400

        if new_block.hash != new_block.calculate_hash():
            return jsonify({"message": "Invalid block hash"}), 400

        # Možeš dodati proveru da li hash zadovoljava difficulty...

        blockchain.chain.append(new_block)
        blockchain.save_chain()
        mempool.clear_transactions(block_data['transactions'])
        broadcast_block(block_data)

        return jsonify({"message": "Block added to chain"}), 201
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 400


@app.route('/peers', methods=['GET'])
def get_peers():
    return jsonify(list(peers))


@app.route('/add_peer', methods=['POST'])
def add_peer():
    peer_data = request.get_json()
    peer = peer_data.get('peer')
    if peer and peer not in peers:
        peers.add(peer)
        return jsonify({"message": "Peer added"}), 201
    else:
        return jsonify({"message": "Invalid peer or already exists"}), 400


# ----------------- P2P helper functions -----------------

def broadcast_transaction(tx):
    for peer in peers:
        try:
            requests.post(f"http://{peer}/transaction", json=tx, timeout=3)
        except:
            pass


def broadcast_block(block):
    for peer in peers:
        try:
            requests.post(f"http://{peer}/block", json=block, timeout=3)
        except:
            pass


def sync_chain():
    global blockchain
    max_length = len(blockchain.chain)
    new_chain = None

    for peer in peers:
        try:
            response = requests.get(f"http://{peer}/blockchain", timeout=3)
            if response.status_code == 200:
                data = response.json()
                length = data['length']
                chain_data = data['chain']
                if length > max_length:
                    temp_chain = []
                    for block_data in chain_data:
                        txs = [Transaction(**tx) for tx in block_data['transactions']]
                        block = blockchain.chain[-1].__class__(
                            index=block_data['index'],
                            transactions=txs,
                            previous_hash=block_data['previous_hash'],
                            nonce=block_data['nonce'],
                            timestamp=block_data['timestamp'],
                            hash=block_data['hash']
                        )
                        temp_chain.append(block)
                    max_length = length
                    new_chain = temp_chain
        except:
            continue

    if new_chain:
        blockchain.chain = new_chain
        blockchain.save_chain()
        print("[SYNC] Blockchain synchronized with peers")


def sync_mempool():
    global mempool
    for peer in peers:
        try:
            response = requests.get(f"http://{peer}/mempool", timeout=3)
            if response.status_code == 200:
                txs = response.json()
                for tx in txs:
                    if not mempool.has_transaction(tx):
                        mempool.add_transaction(tx)
        except:
            pass


def run_sync_loop():
    while True:
        sync_chain()
        sync_mempool()
        time.sleep(10)


# ----------------- Auto mining thread -----------------

def run_auto_mining(miner_address):
    miner = Miner(miner_address)
    while True:
        if mempool.get_transactions():
            print("[MINER] Mining new block...")
            new_hash = miner.mine_pending_transactions()
            if new_hash:
                print(f"[MINER] Block mined with hash: {new_hash}")
            else:
                print("[MINER] No valid nonce found.")
        else:
            print("[MINER] No transactions to mine, sleeping...")
        time.sleep(15)


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 3:
        print("Usage: python node.py [port] [miner_wallet_name]")
        exit(1)

    port = int(sys.argv[1])
    miner_wallet_name = sys.argv[2]

    # Kreiraj wallet za rudara (ako već ne postoji)
    miner_wallet = Wallet(miner_wallet_name)

    # Početni peer-ovi (ručno ili učitati iz fajla)
    # Primer: peers.add("127.0.0.1:5001")
    # Peers možeš dodavati i na API /add_peer

    # Start pozadinskih poslova
    threading.Thread(target=run_sync_loop, daemon=True).start()
    threading.Thread(target=run_auto_mining, args=(miner_wallet.get_address(),), daemon=True).start()

    app.run(host='0.0.0.0', port=port)
