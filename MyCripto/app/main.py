import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.wallet import Wallet
from core.blockchain import Blockchain
from core.transaction import Transaction

from core.mempool import Mempool
from core.miner import Miner

def create_wallet():
    try:
        name = input("Enter wallet name: ").strip()
        if not name:
            print("Wallet name cannot be empty.")
            input("Press Enter to continue...")
            return

        wallet = Wallet(name)
        bc = Blockchain()
        balance = bc.get_balance(wallet.get_address())

        print(f"\n✅ Wallet created/loaded: {name}")
        print(f"🏦 Address: {wallet.get_address()}")
        print(f"💰 Balance: {balance} MB\n")
        input("Press Enter to continue...")

    except Exception as e:
        print(f"❌ Error creating wallet: {e}")
        input("Press Enter to continue...")

def send_coins():
    try:
        sender_name = input("Sender wallet name: ").strip()
        recipient_address = input("Recipient address: ").strip()
        if not sender_name or not recipient_address:
            print("❌ Sender or recipient cannot be empty.")
            input("Press Enter to continue...")
            return

        amount = float(input("Amount to send: ").strip())
        if amount <= 0:
            print("❌ Amount must be positive.")
            input("Press Enter to continue...")
            return

        sender = Wallet(sender_name)
        bc = Blockchain()
        balance = bc.get_balance(sender.get_address())

        if balance < amount:
            print(f"❌ Not enough balance! You have {balance} MB")
            input("Press Enter to continue...")
            return

        tx = Transaction(
            sender=sender.get_address(),
            recipient=recipient_address,
            amount=amount
        )
        tx.sign(sender.private_key)

        if not tx.is_valid():
            print("❌ Invalid transaction signature.")
            input("Press Enter to continue...")
            return

        mempool = Mempool()
        mempool.add_transaction(tx.to_dict())

        print("✅ Transaction added to mempool!")
        input("Press Enter to continue...")

    except ValueError:
        print("❌ Invalid amount. Please enter a number.")
        input("Press Enter to continue...")
    except Exception as e:
        print(f"❌ Error: {e}")
        input("Press Enter to continue...")

def view_blockchain():
    try:
        bc = Blockchain()
        print("\n--- Blockchain ---")
        for block in bc.chain:
            print(f"\n🧱 Block #{block.index}")
            print(f"🔗 Hash: {block.hash}")
            print(f"⬆️ Previous Hash: {block.previous_hash}")
            print("📦 Transactions:")
            for tx in block.transactions:
                print(f"  From: {tx.sender[:15]}... ➡️ To: {tx.recipient[:15]}... 💸 {tx.amount} MB")
            print("-" * 40)
        input("Press Enter to continue...")
    except Exception as e:
        print(f"❌ Error viewing blockchain: {e}")
        input("Press Enter to continue...")

def mine_block():
    try:
        miner_name = input("Enter miner wallet name: ").strip()
        if not miner_name:
            print("❌ Miner name cannot be empty.")
            input("Press Enter to continue...")
            return

        miner_wallet = Wallet(miner_name)
        miner = Miner(miner_wallet.get_address())

        print("⛏️ Mining block... (this may take a while)")
        new_hash = miner.mine_pending_transactions()

        if new_hash:
            print(f"✅ Block successfully mined! 🔗 Hash: {new_hash}")
        else:
            print("ℹ️ No transactions in mempool to mine.")

        input("Press Enter to continue...")

    except Exception as e:
        print(f"❌ Error mining block: {e}")
        input("Press Enter to continue...")

def mine_block_real():
    try:
        miner_name = input("Enter miner wallet name: ").strip()
        if not miner_name:
            print("❌ Miner name cannot be empty.")
            input("Press Enter to continue...")
            return

        miner_wallet = Wallet(miner_name)
        miner = Miner(miner_wallet.get_address())

        duration = input("Enter mining duration in seconds (e.g. 20): ").strip()
        try:
            duration = int(duration)
            if duration <= 0:
                raise ValueError()
        except ValueError:
            print("❌ Invalid duration, using default 20 seconds.")
            duration = 20

        print(f"⛏️ Real mining started for {duration} seconds...")
        new_hash = miner.mine_with_time_limit(duration_seconds=duration)

        if new_hash:
            print(f"✅ Block successfully mined! 🔗 Hash: {new_hash}")
        else:
            print("ℹ️ No valid nonce found in given time.")

        input("Press Enter to continue...")

    except Exception as e:
        print(f"❌ Error during real mining: {e}")
        input("Press Enter to continue...")

def check_balance():
    try:
        name = input("Enter your wallet name: ").strip()
        if not name:
            print("❌ Wallet name cannot be empty.")
            input("Press Enter to continue...")
            return

        wallet = Wallet(name)
        bc = Blockchain()
        balance = bc.get_balance(wallet.get_address())
        print(f"💰 Balance for wallet '{name}': {balance} MB")
        input("Press Enter to continue...")

    except Exception as e:
        print(f"❌ Error checking balance: {e}")
        input("Press Enter to continue...")

def main_menu():
    menu = {
        "1": ("🆕 Create Wallet", create_wallet),
        "2": ("💸 Send Coins", send_coins),
        "3": ("📜 View Blockchain", view_blockchain),
        "4": ("⛏️ Mine Block (fast mining)", mine_block),
        "5": ("📊 Check Balance", check_balance),
        "6": ("⛏️ Real Mining (time-limited nonce solving)", mine_block_real),
        "7": ("🚪 Exit", None)
    }

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n===== 💰 MineByte CLI Wallet =====")
        for key, (desc, _) in menu.items():
            print(f"{key}. {desc}")

        choice = input("Choose option: ").strip()
        if choice not in menu:
            print("❌ Invalid option!")
            input("Press Enter to continue...")
            continue

        if choice == "7":
            print("👋 Goodbye!")
            break

        _, action = menu[choice]
        action()

if __name__ == "__main__":
    main_menu()
