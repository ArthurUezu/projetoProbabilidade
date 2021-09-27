from pandas.core.algorithms import duplicated
import requests
import pandas as pd
from bs4 import BeautifulSoup

palavras_chave = ("corona","coronavirus","covid","sars-cov-2") #
url_base = "https://www.e-farsas.com/page/"
url_final = "?s="
url_site = "https://www.e-farsas.com/page/1?s="

dados = []

for palavra in palavras_chave:
    response = requests.get(url_site+palavra)
    site = BeautifulSoup(response.text,'html.parser')
    noticias = site.find_all('div',attrs={'class':'td-module-meta-info'})
    for i in range(0, 12):
        titulo = noticias[i].find('a',attrs={'rel':'bookmark'})
        data = noticias[i].find('time')
        categoria = noticias[i].find('a',attrs={'class':'td-post-category'})
        # print(data.text)
        dados.append([titulo.text,data.text])

dados = pd.DataFrame(dados,columns=['titulo','data']).drop_duplicates()
print(dados)
dados.to_csv("efarsas.csv",index=False)