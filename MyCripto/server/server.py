# server/server.py

import sys
import os

# Dodaj root folder (jedan nivo iznad server/) u sys.path da bi mogao da importuješ core module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.blockchain import Blockchain
from core.transaction import Transaction
from core.wallet import Wallet
from core.mempool import Mempool
from core.miner import Miner

import socket
import threading
import json

HOST = '127.0.0.1'  # localhost, promeni ako treba
PORT = 65432        # bilo koji slobodan port

blockchain = Blockchain()
mempool = Mempool()

def handle_client(conn, addr):
    print(f"Connected by {addr}")
    try:
        while True:
            data = conn.recv(4096)
            if not data:
                break
            request = json.loads(data.decode())

            action = request.get("action")
            if action == "get_balance":
                address = request.get("address")
                balance = blockchain.get_balance(address)
                response = {"status": "success", "balance": balance}
            elif action == "send_transaction":
                tx_data = request.get("transaction")
                tx = Transaction(**tx_data)
                if not tx.is_valid():
                    response = {"status": "error", "message": "Invalid transaction signature"}
                else:
                    mempool.add_transaction(tx.to_dict())
                    response = {"status": "success", "message": "Transaction added to mempool"}
            elif action == "mine":
                miner_address = request.get("miner_address")
                miner = Miner(miner_address)
                new_hash = miner.mine_pending_transactions()
                if new_hash:
                    response = {"status": "success", "message": f"New block mined: {new_hash}"}
                else:
                    response = {"status": "error", "message": "No transactions to mine"}
            elif action == "get_chain":
                # Serialize blockchain data to send back
                chain_data = [{
                    "index": block.index,
                    "previous_hash": block.previous_hash,
                    "hash": block.hash,
                    "nonce": block.nonce,
                    "timestamp": block.timestamp,
                    "transactions": [tx.to_dict() for tx in block.transactions]
                } for block in blockchain.chain]
                response = {"status": "success", "chain": chain_data}
            else:
                response = {"status": "error", "message": "Unknown action"}

            conn.sendall(json.dumps(response).encode())
    except Exception as e:
        print(f"Error handling client {addr}: {e}")
    finally:
        conn.close()

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()

if __name__ == "__main__":
    start_server()
