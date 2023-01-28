import json
import socket
import requests
from config import secrets, HOST, PORT


s = socket.socket()
s.bind((HOST, PORT))
print(f"Aguardando conexão na porta: {PORT}")

s.listen(5)
connection, address = s.accept()
print(f"Recebendo solicitação de {address}")

bearer_token = secrets["bearer_token"]

keyword = "lula"

url_rules = "https://api.twitter.com/2/tweets/search/stream/rules"
header = {'Authorization': f"Bearer {bearer_token}"}
response = requests.post(
    url_rules,
    headers=header,
    json={"add": [{"value": keyword}]}
)

url = "https://api.twitter.com/2/tweets/search/stream"
response = requests.get(url, headers=header, stream=True)

if response.status_code == 200:
    for item in response.iter_lines():
        try:
            print(json.loads(item)["data"]["text"])
            print("="*50)
            connection.send(json.loads(item)["data"]["text"].encode("latin1", "ignore"))
        except:
            continue

connection.close()