# 💰 MineByte (MB) — CLI Cryptocurrency Wallet & Blockchain

MineByte (MB) is a lightweight, educational cryptocurrency project implemented in Python. It demonstrates the core concepts of blockchain technology including wallets, transactions, mining, and a persistent blockchain system — all through a simple command-line interface.

---

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

## 🧰 Getting Started

### ✅ Prerequisites

- Python 3.7 or higher
- (Optional but recommended) Virtual environment

### 🔧 Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/minebyte.git
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
💡 Note: This project currently has minimal or no external dependencies.

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

📚 Usage Overview
🧾 Create Wallet
Generate or load a wallet by name. A key pair is created and saved locally.

💸 Send Coins
Transfer MB coins to another wallet’s public address using digital signatures.

🔍 View Blockchain
See all mined blocks with their transactions, hashes, and references.

⛏️ Mine Blocks
Use Proof-of-Work to confirm transactions. Choose between:

Fast Mining — Mines instantly (for testing)

Real Mining — Simulates actual mining with time-based nonce searching

Mining rewards are credited to the miner’s wallet.

💰 Check Balance
Enter your wallet name to compute balance from all past transactions.

📁 Project Structure
plaintext
Copy
Edit
minebyte/
├── app/
│   ├── data/
│   │   ├── __init__.py
│   │   └── main.py               # CLI Entry Point
│
├── Client/                       # (Unused or WIP)
│
├── config/
│   ├── settings.py               # Configuration (difficulty, reward, file paths)
│
├── core/
│   ├── __init__.py
│   ├── blockchain.py             # Blockchain and block logic
│   ├── mempool.py                # Pending transactions
│   ├── miner.py                  # Mining logic
│   ├── node.py                   # Network node logic
│   ├── transaction.py            # Transaction creation & verification
│   └── wallet.py                 # Wallet key generation and loading
│
├── data/
│   ├── blockchain.json           # Saved blockchain
│   ├── mempool.json              # Saved mempool
│   └── wallets.json              # Saved wallets
│
├── server/
│   ├── data/
│   └── server.py                 # Server logic (if implemented)
│
├── tests/
│   └── test_blockchain.py        # Unit tests
│
├── utils/
│   ├── __init__.py
│   ├── crypto_utils.py           # Key generation and hashing
│   └── file_io.py                # JSON file handling
│
└── .gitignore
🤝 Contributing
Contributions are welcome! Feel free to open issues or submit pull requests.

📜 License
This project is licensed under the MIT License. See the LICENSE file for details.

🙏 Acknowledgements
Inspired by Bitcoin and educational blockchain demos.
Created by [Zypher0903].
