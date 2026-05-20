import urllib.request

url = input("Enter URL to fetch: ")
response = urllib.request.urlopen(url)
print(response.read()[:200])
