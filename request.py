import requests

r = requests.get('http://127.0.0.1:5000/')

print(r.status_code)

dict_resp = r.json()

for resp in dict_resp:
    print(f'''
        Titulo: {resp['Titulo']},
        Preço: {resp['Preço']}
        Descrição: {resp['Descrição']},
        Avaliação: {resp['Avaliaçoes']},
        Estrelas: {resp['Estrelas']},
        ''')