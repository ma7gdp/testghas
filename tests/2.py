from Crypto.Cipher import ARC4

key = b"secretkey"
ciphertext = b"\x12\x34\x56\x78"

cipher = ARC4.new(key)
plaintext = cipher.decrypt(ciphertext)
print(plaintext)
