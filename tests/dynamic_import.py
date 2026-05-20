import importlib

module_name = input("Enter module name: ")
module = importlib.import_module(module_name)
print(module)
