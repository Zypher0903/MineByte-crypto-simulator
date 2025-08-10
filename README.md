💰 MineByte (MB) — CLI Cryptocurrency Wallet & Blockchain
MineByte (MB) is a lightweight, educational cryptocurrency project implemented in Python. It demonstrates core blockchain concepts such as wallets, cryptographically signed transactions, mining, and a persistent blockchain, all through a user-friendly command-line interface.

MineByte converter: https://bright-elf-2fde17.netlify.app/
Discord server: https://discord.gg/tz3JMEhj

🚀 Features
🔐 Wallet Management: Generate and load wallets using public/private key cryptography.

🔁 Secure Transactions: Send MB coins with cryptographic signatures ensuring authenticity.

⛓️ Immutable Blockchain: Persistent JSON-based blockchain ensures transaction history integrity.

⚒️ Proof-of-Work Mining: Adjustable difficulty mining validates transactions and secures the network.

🧾 Mempool: Transaction pool holding pending transactions before inclusion in blocks.

⏱️ Multiple Mining Modes: Supports fast mining (instant nonce) and realistic time-limited mining.

💵 Balance Queries: View wallet balances reflecting blockchain-confirmed transactions.

🖥️ Intuitive CLI: Interactive menus simplify wallet, transaction, and blockchain management.

🌐 Distributed P2P Network: Multiple MineByte nodes can connect to form a decentralized network supporting cross-node transactions.

🆕 What’s New — Distributed Network Node (node.py)
MineByte now includes a P2P network node implemented with a Flask REST API, enabling multiple instances to connect over HTTP and synchronize blockchain data and transactions.

Key Enhancements:
🌍 Decentralized Network: Nodes communicate to maintain a consistent blockchain.

🔄 Automatic Synchronization: Chains and mempools stay updated across nodes.

📡 Broadcasting: Transactions and mined blocks propagate to all connected peers.

⚙️ Automated Mining: Nodes can mine transactions from their mempool automatically.

🛠️ REST API: Inspect blockchain status, mempool, connected peers, and submit transactions or blocks.

🔗 Cross-node Transactions: Send MB coins securely from wallets on one node to wallets on another seamlessly.

🧰 Usage Guide — Running and Using Nodes
1. Start a Node
bash
Copy
Edit
python core/node.py [port] [miner_wallet_name]
Example:

bash
Copy
Edit
python core/node.py 5000 miner_wallet
This starts a MineByte node listening on port 5000, using miner_wallet for mining rewards.

2. Connect Nodes (Add Peers)
To form a network, nodes must be connected as peers.

Use the /add_peer endpoint to connect nodes:

bash
Copy
Edit
curl -X POST http://localhost:5000/add_peer -H "Content-Type: application/json" -d '{"peer":"localhost:5001"}'
Repeat on other nodes with appropriate addresses to build a mesh network.

3. Create or Load Wallets
Manage wallets on any node through the CLI (app/main.py) or via API endpoints.

4. Sending MB Coins Across the Network
Via CLI:
Choose Send Coins and input:

Sender wallet name

Recipient wallet address (can be from any node)

Amount of MB to send

Via API:
Submit transaction data as JSON to the /transaction endpoint on any node.

Transactions are broadcasted to all peers and pooled for mining.

5. Mining Transactions
Mine blocks manually via CLI or enable automated mining on nodes with a miner wallet.

Mining confirms transactions network-wide by adding them to the blockchain.

6. Checking Balances
Query any node to check wallet balances, which reflect the network’s confirmed blockchain state.

🔍 What You Can Do Now
Deploy multiple MineByte nodes on different machines or ports to create a decentralized blockchain network.

Securely transfer MB coins between wallets anywhere within the connected network.

Enjoy automatic transaction validation, mempool sharing, and synchronized mining.

Use REST APIs to monitor blockchain data, mempool contents, and peer connections.

📅 Future Plans
🔄 Automatic peer discovery for easy network scaling.

🔐 Secure, encrypted communications between nodes.

📱 User-friendly frontends (web/desktop) for easier wallet and node management.

⛓️ Advanced consensus algorithms for increased security.

🔗 Cross-chain interoperability and external integrations.

🧪 Testnets and network simulators for development.

🧰 Getting Started
Prerequisites
Python 3.7+

(Recommended) Virtual environment

Installation
bash
Copy
Edit
git clone https://github.com/Zypher0903/minebyte.git
cd minebyte
python -m venv venv
# Activate environment
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
pip install -r requirements.txt
▶️ Running the CLI Wallet
Launch the wallet interface:

bash
Copy
Edit
python app/main.py
Interact with the menu to:

Create/load wallets

Send MB coins

View the blockchain

Mine blocks

Check balances

Exit

⚠️ Important Disclaimer
MineByte is an educational project for learning blockchain fundamentals.

Not connected to public blockchains or exchanges.

MB coins have no real-world market value or guaranteed liquidity.

Any real-money exchanges are outside this system and subject to personal agreement.

Not financial advice — use responsibly and for education only.

🤝 Contributing
Contributions, bug reports, and feature requests are welcome! Please open issues or pull requests.

📜 License
Licensed under the MIT License. See LICENSE for details.

🙏 Acknowledgements
Inspired by Bitcoin and educational blockchain projects.
Created by [Zypher0903].

