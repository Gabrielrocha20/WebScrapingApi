import time
from operator import attrgetter, itemgetter

import playwright
from flask import Flask, jsonify
from playwright.sync_api import expect, sync_playwright


def get_dados():
    with sync_playwright() as p:

        precos = []
        produtos_precos = []
        produtos = []

        estrelas = []
        numero_avaliacoes = []

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
            estrela = pagina.locator(f'xpath=/html/body/div[1]/div[3]/div/div[2]/div/div[{count}]/div/div[2]/p[2]').inner_html()
            avaliacoes = pagina.locator(f'xpath=/html/body/div[1]/div[3]/div/div[2]/div/div[{count}]/div/div[2]/p[1]').inner_text()
            

            page = pagina.locator(f'xpath={xpath_title}').element_handles()
            for teste in page:
                if 'Lenovo' in teste.inner_text():
                    estrela = estrela.split('\n\t\t\t\t\t\t\t')
                    for index, e in enumerate(estrela):
                        if len(e) <1:
                            estrela.pop(index)
                        else:
                            estrela[index] = e.replace('\t', '')
                    estrelas.append(len(estrela))
                    numero_avaliacoes.append(avaliacoes)
                    produtos_precos.append(precos[count - 1])
            count += 1

            
        sites = pagina.get_by_text('Lenovo').element_handles()
        produtos_precos.pop(1)
        estrelas.pop(1)
        numero_avaliacoes.pop(1)
        
        index = 0
        for produto in sites:
            produto_lista = produto.inner_text().split(',')
            if len(produto_lista) > 1:
                try:
                    produto_lista.append(produtos_precos[index])
                    produto_lista.append(numero_avaliacoes[index])
                    produto_lista.append(estrelas[index])
                    produtos.append(produto_lista)
                    index += 1
                except IndexError as e:
                    break
        return produtos


app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False
app.config['JSON_SORT_KEYS'] = False

@app.route('/')
def apiPage():
    resposta = []
    produtos = get_dados()
    produtos = sorted(produtos, key=itemgetter(-3))

    for produto in produtos:
        resposta.append({
            'Titulo':produto[0],
            'Descrição': ' '.join(produto[:-3]),
            'Preço': produto[-3],
            'Avaliaçoes': produto[-2],
            'Estrelas': produto[-1]
        })
    return jsonify(resposta)


app.run()

# /html/body/div[1]/div[3]/div/div[2]/div/div[1]/div/div[1]/h4[2]/a
# /html/body/div[1]/div[3]/div/div[2]/div/div[2]/div/div[1]/h4[2]/a