import pickle

payload = input("Enter pickle payload: ")
obj = pickle.loads(payload.encode("utf-8"))
print(obj)
