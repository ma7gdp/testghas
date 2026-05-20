import subprocess

user_arg = input("Enter directory: ")
subprocess.run(["ls", user_arg])
