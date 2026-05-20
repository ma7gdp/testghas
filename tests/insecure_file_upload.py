filename = input("Upload filename: ")
content = input("File content: ")
with open("/tmp/uploads/" + filename, "w") as fp:
    fp.write(content)
