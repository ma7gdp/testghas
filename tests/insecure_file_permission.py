import os

path = "/tmp/secret.txt"
with open(path, "w") as fp:
    fp.write("secret data")
os.chmod(path, 0o777)
