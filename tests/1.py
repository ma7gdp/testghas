import hashlib

data = b"something"
sha1_obj = hashlib.sha1(data)

# Raw bytes
digest_bytes = sha1_obj.digest()
print(digest_bytes)

# Hex string
digest_hex = sha1_obj.hexdigest()
print(digest_hex)