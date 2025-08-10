💰 MineByte (MB) — CLI Cryptocurrency Wallet & Blockchain
MineByte (MB) is a lightweight, educational cryptocurrency project implemented in Python. It demonstrates the core concepts of blockchain technology including wallets, transactions, mining, and a persistent blockchain system — all through a simple command-line interface.

MineByte converter: https://bright-elf-2fde17.netlify.app/
Discord server link: https://discord.gg/tz3JMEhj

🚀 Features
🔐 Wallet Management — Create and load wallets with public/private key pairs.

🔁 Transactions — Send MB coins securely with cryptographic signatures.

⛓️ Blockchain — Immutable, persistent blockchain stored as JSON.

⚒️ Mining — Proof-of-work mining with adjustable difficulty.

🧾 Mempool — Pool of pending transactions awaiting confirmation.

⏱️ Multiple Mining Modes — Fast mining (instant nonce solving) and real-time mining.

💵 Balance Checking — Query wallet balances based on blockchain history.

🖥️ CLI Interface — Simple command-line interface with interactive menus.

🌐 Distributed P2P Network — Nodes communicate over HTTP to synchronize blockchain and mempool.

🆕 What’s New — Network Node (node.py)
MineByte now supports a distributed peer-to-peer network node implemented via Flask REST API, enabling multiple MineByte instances to interconnect and form a decentralized blockchain network.

New capabilities with node.py:
🌐 Peer-to-peer networking — Connect multiple nodes (peers) over HTTP.

🔄 Blockchain & mempool synchronization — Nodes automatically sync their chains and transaction pools.

💸 Transaction and block broadcasting — Transactions and newly mined blocks propagate through the network.

⚡ Automated mining — Nodes can mine blocks automatically based on mempool contents.

🔍 REST API endpoints for inspecting blockchain state, mempool, peers, and submitting transactions or blocks.

🧰 How to Use node.py — Step by Step
Start a node:

bash
Copy
Edit
python core/node.py [port] [miner_wallet_name]
Example:

bash
Copy
Edit
python core/node.py 5000 my_miner_wallet
Connect nodes (peers):

Add peers by sending a POST request to /add_peer endpoint:

bash
Copy
Edit
curl -X POST http://localhost:5000/add_peer -H "Content-Type: application/json" -d '{"peer":"localhost:5001"}'
Create or load wallets:

Use the CLI interface (app/main.py) or API to manage wallets.

Send transactions:

Send MB coins via CLI or HTTP POST /transaction. Transactions propagate across all nodes.

Mining:

Nodes mine blocks manually (via CLI) or automatically if configured with a miner wallet.

Check balances:

Query the blockchain state at any node to check wallet balances.

💸 How to Send and Use MineByte (MB)
Creating wallets:
Use the CLI to generate wallets with secure cryptographic key pairs.

Sending MB coins:

Via CLI: Select the send option, enter sender wallet, recipient wallet address, and amount.

Via API: Submit transaction data with sender, recipient, amount, and signature to /transaction.

Transaction confirmation:
Transactions enter the mempool, then are included in newly mined blocks, confirming the transfer.

Checking balances:
Balances are derived from confirmed transactions recorded on the blockchain.

Using MB for exchange:
MB coins currently have no official market value. Users can agree externally to trade MB for goods or services. Transactions are securely recorded on the blockchain to prevent fraud.

🧰 Getting Started
✅ Prerequisites
Python 3.7 or higher

(Optional) Virtual environment recommended

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
Start the wallet interface with:

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
MineByte (MB) is an educational and local project designed to demonstrate the principles of blockchain technology and mining.

MineByte is not connected to any public blockchain or exchange.

MB coins have no market price and no guaranteed liquidity.

MB is used only within this local blockchain network.

Any real-world exchange of MB coins must be done outside this system by personal agreement.

This project is not financial advice or an investment. Use responsibly and for educational purposes only.

🤝 Contributing
Contributions are welcome! Please open issues or submit pull requests to improve MineByte.

📜 License
This project is licensed under the MIT License. See the LICENSE file for details.

🙏 Acknowledgements
Inspired by Bitcoin and educational blockchain demos.
Created by [Zypher0903].
