import yaml

payload = input("Enter YAML payload: ")
obj = yaml.unsafe_load(payload)
print(obj)
