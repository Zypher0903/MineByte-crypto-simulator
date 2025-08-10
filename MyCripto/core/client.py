import sys
import requests
from core.wallet import Wallet
from core.transaction import Transaction

TARGET_NODE = "http://127.0.0.1:5000"  # promeni port ako treba

def send_signed_transaction(sender_wallet_name, recipient_address, amount):
    wallet = Wallet(sender_wallet_name)

    tx = Transaction(
        sender=wallet.get_address(),
        recipient=recipient_address,
        amount=amount
    )

    # Potpisujemo baš string koji transaction proverava (get_message)
    signature = wallet.sign_message_str(tx.get_message())
    tx.signature = signature

    tx_data = tx.to_dict()

    try:
        r = requests.post(f"{TARGET_NODE}/transaction", json=tx_data)
        print(f"Status: {r.status_code}")
        print("Odgovor:", r.text)
    except Exception as e:
        print("Greška pri slanju:", e)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Upotreba: python -m core.client <sender_wallet_name> <recipient_public_key> <amount>")
        sys.exit(1)

    sender_wallet_name = sys.argv[1]
    recipient = sys.argv[2]
    amount = int(sys.argv[3])

    send_signed_transaction(sender_wallet_name, recipient, amount)
