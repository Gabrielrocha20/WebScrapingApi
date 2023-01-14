import requests

link = 'http://127.0.0.1:5000/'

requisicao = requests.get(link)
print(requisicao)

corpo = requisicao.json()

print(corpo[0])