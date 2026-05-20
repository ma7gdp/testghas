import ssl
import urllib.request

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
url = input("Enter URL: ")
with urllib.request.urlopen(url, context=ctx) as resp:
    print(resp.read(100))
