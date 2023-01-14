import time
from operator import attrgetter, itemgetter

import playwright
from flask import Flask, jsonify
from playwright.sync_api import expect, sync_playwright

with sync_playwright() as p:

    precos = []
    produtos_precos = []
    produtos = []

    navegador = p.chromium.launch()
    pagina = navegador.new_page()
    pagina.goto("https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops")

    tamanho = pagina.locator('xpath=/html/body/div[1]/div[3]/div/div[2]/div').all_inner_texts()[0].split('reviews')
    
    preco = pagina.get_by_role("heading", name="$",).element_handles()

    for i, texto in enumerate(preco):
        precos.append(float(texto.inner_text()[1:]))

    count = 1

    while count < len(tamanho):
        xpath_title = f'/html/body/div[1]/div[3]/div/div[2]/div/div[{count}]/div/div[1]/h4[2]/a'
        p = pagina.locator(f'xpath={xpath_title}').element_handles()
        for teste in p:
            if 'Lenovo' in teste.inner_text():
                produtos_precos.append(precos[count - 1])
        count += 1

        
    sites = pagina.get_by_text('Lenovo').element_handles()
    produtos_precos.pop(1)
    
    index = 0
    for produto in sites:
        produto_lista = produto.inner_text().split(',')
        if len(produto_lista) > 1:
            try:
                produto_lista.append(produtos_precos[index])
                produtos.append(produto_lista)
                index += 1
            except IndexError as e:
                break

di = []

produtos = sorted(produtos, key=itemgetter(-1))
for p in produtos:
    di.append({
        'Titulo':p[0],
        'Descrição': ' '.join(p[:-2]),
        'Preço': p[-1]
    })



app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False
app.config['JSON_SORT_KEYS'] = False

@app.route('/')
def apiPage():
    resposta = []

    for produto in produtos:
        resposta.append({
            'Titulo':produto[0],
            'Descricao': ' '.join(produto[:-1]),
            'Preco': produto[-1]
        })
    return jsonify(resposta)


app.run(host='0.0.0.0')

# /html/body/div[1]/div[3]/div/div[2]/div/div[1]/div/div[1]/h4[2]/a
# /html/body/div[1]/div[3]/div/div[2]/div/div[2]/div/div[1]/h4[2]/a