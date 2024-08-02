import requests

url = "http://127.0.0.1:5000/stream"
response = requests.get(url, stream=True)

for line in response.iter_lines():
    if line:
        print(line.decode('utf-8'))
