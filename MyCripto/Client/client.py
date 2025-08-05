import requests

API_URL = "http://127.0.0.1:5000"

def create_transaction():
    sender = input("Sender wallet: ").strip()
    recipient = input("Recipient wallet: ").strip()
    try:
        amount = float(input("Amount to send: ").strip())
    except ValueError:
        print("Invalid amount.")
        return

    data = {
        "sender": sender,
        "recipient": recipient,
        "amount": amount
    }

    response = requests.post(f"{API_URL}/transactions/new", json=data)

    if response.status_code == 201:
        print("✅ Transaction added.")
    else:
        print("❌ Error:", response.text)

def mine_block():
    miner = input("Enter your wallet name to mine: ").strip()
    data = {"miner": miner}
    response = requests.post(f"{API_URL}/mine", json=data)
    
    if response.status_code == 200:
        print("⛏️", response.json()["message"])
    else:
        print("❌ Error:", response.text)

def view_blockchain():
    response = requests.get(f"{API_URL}/chain")
    chain = response.json().get("chain", [])
    for block in chain:
        print(f"\n📦 Block #{block['index']}")
        print("   Previous Hash:", block["previous_hash"])
        print("   Transactions:", block["transactions"])
        print("   Nonce:", block["nonce"])
        print("   Hash:", block["hash"])

def check_balance():
    wallet = input("Wallet name: ").strip()
    response = requests.get(f"{API_URL}/balance/{wallet}")
    if response.status_code == 200:
        balance = response.json().get("balance", 0)
        print(f"💰 Balance for '{wallet}': {balance} MB")
    else:
        print("❌ Error:", response.text)

def main():
    while True:
        print("\n===== MineByte CLI Client =====")
        print("1. Send Coins")
        print("2. Mine Block")
        print("3. View Blockchain")
        print("4. Check Balance")
        print("5. Exit")
        choice = input("Select option: ").strip()

        if choice == "1":
            create_transaction()
        elif choice == "2":
            mine_block()
        elif choice == "3":
            view_blockchain()
        elif choice == "4":
            check_balance()
        elif choice == "5":
            print("👋 Goodbye.")
            break
        else:
            print("❌ Invalid choice.")

if __name__ == "__main__":
    main()
