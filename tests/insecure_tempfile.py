import tempfile

filename = tempfile.mktemp()
with open(filename, 'w') as fp:
    fp.write('temporary data')
print(filename)
