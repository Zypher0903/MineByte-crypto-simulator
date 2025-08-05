# utils/crypto_utils.py

import hashlib
import ecdsa
import base64

def sha256(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()

def generate_keys():
    private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
    public_key = private_key.get_verifying_key()
    return (
        private_key.to_string().hex(),
        public_key.to_string().hex()
    )

def sign_data(private_key_hex: str, data: str) -> str:
    sk = ecdsa.SigningKey.from_string(bytes.fromhex(private_key_hex), curve=ecdsa.SECP256k1)
    signature = sk.sign(data.encode())
    return base64.b64encode(signature).decode()

def verify_signature(public_key_hex: str, data: str, signature_b64: str) -> bool:
    try:
        vk = ecdsa.VerifyingKey.from_string(bytes.fromhex(public_key_hex), curve=ecdsa.SECP256k1)
        return vk.verify(base64.b64decode(signature_b64), data.encode())
    except:
        return False
