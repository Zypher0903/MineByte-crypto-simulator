# core/wallet.py

import os
import json
from utils.crypto_utils import generate_keys
from config import settings


def _get_data_path() -> str:
    """
    Vrati apsolutnu putanju do data/wallets.json
    (radi bez obzira na trenutni working-dir).
    """
    # base_dir = folder u kome je cijeli projekt (jedan nivo iznad /core)
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok=True)              # kreiraj data/ ako ga nema
    return os.path.join(data_dir, "wallets.json")


class Wallet:
    def __init__(self, wallet_name: str):
        self.wallet_name = wallet_name
        self.wallet_file = _get_data_path()           # uvijek apsolutna putanja
        self.wallets = self._load_wallets()

        self.private_key = None
        self.public_key  = None
        self.balance     = 0

        if wallet_name in self.wallets:
            data = self.wallets[wallet_name]
            self.private_key = data["private_key"]
            self.public_key  = data["public_key"]
            self.balance     = data["balance"]
        else:
            self._create_wallet()

    # ---------- internals ---------- #
    def _load_wallets(self) -> dict:
        """Učitaj postojeće wallet-e ili vrati prazan dict"""
        if not os.path.exists(self.wallet_file):
            # kreiraj prazan JSON fajl
            with open(self.wallet_file, "w") as f:
                json.dump({}, f)
            return {}
        with open(self.wallet_file, "r") as f:
            content = f.read().strip()
            return json.loads(content) if content else {}

    def _save_wallets(self):
        """Snimi kompletan dict wallet-a u wallets.json"""
        self.wallets[self.wallet_name] = {
            "private_key": self.private_key,
            "public_key":  self.public_key,
            "balance":     self.balance
        }
        with open(self.wallet_file, "w") as f:
            json.dump(self.wallets, f, indent=4)

    def _create_wallet(self):
        """Generiraj ključeve, daj početni balans i snimi"""
        self.private_key, self.public_key = generate_keys()
        self.balance = settings.INITIAL_BALANCE
        self._save_wallets()

    # ---------- javne metode ---------- #
    def get_address(self) -> str:
        return self.public_key

    def get_balance(self) -> float:
        return self.balance
