# -*- coding: utf-8 -*-
"""RSA.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/12t6Tq3ihaPz6gE5tXLETszyNfR3hFGWv
"""

import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding

# Generate Alice's RSA key pair.
alice_private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)
alice_public_key = alice_private_key.public_key()

# Generate Bob's RSA key pair.
bob_private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)
bob_public_key = bob_private_key.public_key()

# Alice generates a symmetric key to share with Bob.
symmetric_key = os.urandom(32)  # 256-bit key

# Alice encrypts the symmetric key with Bob's public key.
encrypted_key = bob_public_key.encrypt(
    symmetric_key,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# Bob decrypts the symmetric key with his private key.
decrypted_key = bob_private_key.decrypt(
    encrypted_key,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# Verify that the decrypted key matches the original symmetric key.
assert decrypted_key == symmetric_key

# Print the shared symmetric key (for demonstration purposes).
print("Symmetric key:", symmetric_key)
print("Decrypted key:", decrypted_key)
