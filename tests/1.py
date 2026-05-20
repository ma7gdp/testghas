import hashlib

session_id = "user-session-12345"
session_bytes = session_id.encode("utf-8")
sha1_obj = hashlib.sha1(session_bytes)

# Raw bytes
digest_bytes = sha1_obj.digest()
print(digest_bytes)

# Hex string
digest_hex = sha1_obj.hexdigest()
print(digest_hex)