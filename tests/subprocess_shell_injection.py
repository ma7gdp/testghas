import subprocess

user_command = input("Enter a command: ")
subprocess.run(user_command, shell=True)
