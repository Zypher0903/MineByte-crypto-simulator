# 💰 MineByte (MB) — CLI Cryptocurrency Wallet & Blockchain

MineByte (MB) is a lightweight, educational cryptocurrency project implemented in Python. It demonstrates the core concepts of blockchain technology including wallets, transactions, mining, and a persistent blockchain system — all through a simple command-line interface.

---

MineByte converter: https://bright-elf-2fde17.netlify.app/

## 🚀 Features

- 🔐 **Wallet Management** — Create and load wallets with public/private key pairs.  
- 🔁 **Transactions** — Send MB coins securely with cryptographic signatures.  
- ⛓️ **Blockchain** — Immutable, persistent blockchain stored as JSON.  
- ⚒️ **Mining** — Proof-of-work mining with adjustable difficulty.  
- 🧾 **Mempool** — Pool of pending transactions awaiting confirmation.  
- ⏱️ **Multiple Mining Modes** — Fast mining (instant nonce solving) and real-time mining.  
- 💵 **Balance Checking** — Query wallet balances based on blockchain history.  
- 🖥️ **CLI Interface** — Simple command-line interface with interactive menus.

---

## 🆕 What’s New — Network Node (`node.py`)

MineByte now supports a **distributed P2P network node** implemented with Flask REST API, enabling multiple MineByte instances to interconnect and form a decentralized blockchain network.

### New capabilities with `node.py`:

- 🌐 **Peer-to-peer network** — Connect multiple nodes (peers) over HTTP.  
- 🔄 **Blockchain synchronization** — Nodes sync their chains and mempools automatically.  
- 💸 **Transaction and block broadcasting** — New transactions and mined blocks propagate through the network.  
- ⚡ **Automated mining** — Nodes can mine blocks automatically based on their mempool contents.  
- 🔍 **REST API endpoints** for inspecting blockchain state, mempool, peers, and submitting transactions or blocks.

---

## 🧰 How to Use `node.py` — Step by Step

1. **Start a node:**

   ```bash
   python core/node.py [port] [miner_wallet_name]
Example:

bash
Copy
Edit
python core/node.py 5000 my_miner_wallet
Add peers to connect nodes:

Use the /add_peer endpoint via HTTP POST to add other nodes, for example:

bash
Copy
Edit
curl -X POST http://localhost:5000/add_peer -H "Content-Type: application/json" -d '{"peer":"localhost:5001"}'
Create or load wallets via the CLI (app/main.py) or API.

Send transactions to any node through CLI or HTTP POST /transaction.

Transactions propagate through the network and get included in blocks mined by any node.

Mining can be done automatically by nodes running a miner wallet, or manually via CLI.

Check balances at any node by querying blockchain state.

🔍 What Is Possible Now?
Run multiple MineByte nodes on different machines or ports to create a decentralized network.

Send MB coins securely between wallets located anywhere with network connectivity.

Automatic transaction validation, mempool sharing, and block mining happen across all connected nodes.

Nodes keep their blockchains and mempools synchronized in near real-time.

Inspect blockchain data, mempool transactions, and connected peers via HTTP REST API.

📅 Upcoming Plans & Features
🔄 Automatic peer discovery for seamless network expansion.

🔐 Encrypted and authenticated network communication for enhanced security.

📱 User-friendly frontend app (web or desktop) for easier wallet and node management.

⛓️ Advanced consensus algorithms to improve security and scalability.

📦 Integration with external systems and cross-chain bridges.

🧪 Testnet environment and network simulators for development and testing.

🧰 Getting Started
✅ Prerequisites
Python 3.7 or higher

(Optional but recommended) Virtual environment

🔧 Installation
Clone the repository:

bash
Copy
Edit
git clone https://github.com/Zypher0903/minebyte.git
cd minebyte
(Optional) Create and activate a virtual environment:

bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies (if any):

bash
Copy
Edit
pip install -r requirements.txt
▶️ Running the CLI Wallet
Run the main script to start the wallet interface:

bash
Copy
Edit
python app/main.py
You will see a menu with options to:

Create wallets

Send coins

View the blockchain

Mine blocks

Check balances

Exit

⚠️ Disclaimer
MineByte (MB) is an educational and local project designed to demonstrate and learn the basic principles of blockchain technology and mining.

It is important to understand that:

MineByte is currently not connected to any public network or official exchange.

The value of MB coins has no market price and is defined solely by agreements between users within this system.

MB is used exclusively within the local blockchain instance and does not guarantee liquidity or convertibility to real currencies.

Any exchange of MineByte coins for real money takes place outside the system and by personal agreement between users.

This project is not financial advice or an investment. Use responsibly and only for educational purposes.

🤝 Contributing
Contributions are welcome! Feel free to open issues or submit pull requests to improve the project.

📜 License
This project is licensed under the MIT License. See the LICENSE file for details.

🙏 Acknowledgements
Inspired by Bitcoin and educational blockchain demos.
Created by [Zypher0903].
