filename = input("Enter filename: ")
with open("/tmp/" + filename, "r") as fp:
    print(fp.read())
