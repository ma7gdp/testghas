import hashlib

password = "secret-password"
print(hashlib.md5(password.encode("utf-8")).hexdigest())
