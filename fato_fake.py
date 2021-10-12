from os import link
from typing import Text
from pandas.core.algorithms import duplicated
import requests
import pandas as pd
import datetime
from bs4 import BeautifulSoup

def tratamentoData(data):
    date = data.split(" ")
    date = date[1]
    date = date.split("/")
    return date

def filtragemCategoria(categoria):
    try:
        if categoria.text=="Conspirações" or categoria.text=="Falso":
            categoria = "Falso"
        else:
            categoria = "Verdadeiro"
    except(AttributeError):
        categoria = "Erro"
    return categoria

mes_dicionario = {'janeiro':1,'fevereiro':2,'março':3,'abril':4,'maio':5,'junho':6,'julho':7,'agosto':8,'setembro':9,'outubro':10,'novembro':11,'dezembro':12}
palavras_chave = ("corona", "coronavirus")#, "sars-cov-2", "covid" 

url_base = "https://g1.globo.com/busca/?q=%23fake+"
url_meio = "&page="
url_final = "&order=recent&species=notícias"

#lista para armazenar os dados recolhidos do site
dados = []

#loop principal do webscraper
for palavra in palavras_chave:
    pagina_atual=1
    paginas_total=2 #2 é apenas para inicializar a variável, o valor dela é alterado no próximo loop
    print('Palavra chave atual: ' + palavra)

    while pagina_atual != int(paginas_total) + 1:
        print(url_base+palavra+url_meio+str(pagina_atual)+url_final)
        response_menu = requests.get(url_base+palavra+url_meio+str(pagina_atual)+url_final) #site + palavra chave
        site_menu = BeautifulSoup(response_menu.text,'html.parser')
        container = site_menu.find('ul', attrs={'class': 'results__list'})
        if(container.find_all('div',attrs={'class':'widget--info__text-container'})): #recolhe cada box de noticia
            noticias = container.find_all('div',attrs={'class':'widget--info__text-container'})
            paginas_total = paginas_total + 1
        print("Pagina:",pagina_atual)
        
        #seleção das informações relevantes
        for noticia in noticias:

            titulo = noticia.find('div',attrs={'class':'widget--info__title'})
            print("Post: " + titulo.text)
            if(titulo.text.__contains__("#FAKE")):
                categoria = "Falso"
            elif(titulo.text.__contains__("#FATO")):
                categoria = "Verdadeiro"
            else:
                categoria = "Inconclusivo"

            link_noticia = noticia.find('a')['href']
            # print(link_noticia)
            response_noticia = requests.get("https:"+link_noticia)
            site_noticia = BeautifulSoup(response_noticia.text,'html.parser')
            link_noticia = site_noticia.find('script')
            link_noticia = str(link_noticia).split('"')
            link_noticia = link_noticia[1]
            response_noticia = requests.get(link_noticia)
            site_noticia = BeautifulSoup(response_noticia.text,'html.parser')
            try:
                noticia_texto = site_noticia.find("article", attrs={"itemprop": "articleBody"})
                noticia_texto = noticia_texto.text
                data = site_noticia.find('time',attrs={'itemprop':'datePublished'})
                data = tratamentoData(data.text)
                if int(data[2]) <= 2019:
                    pagina_atual = int(paginas_total)
                    break
            except (AttributeError):
                noticia_texto = "Error"
                data = ['0','0','0']
            print(data)
            dados.append([link_noticia,titulo.text,categoria,data[0]+'/'+str(data[1])+'/'+data[2],noticia_texto]) #armazenamento dos dados na lista
        pagina_atual = pagina_atual + 1
        print('\n')

#remoção de dados duplicados
dados = pd.DataFrame(dados,columns=['link','titulo','categoria','data','texto']).drop_duplicates()
print(dados)

#armazenamento dos dados em csv
dados.to_csv("fato_fake.csv",index=False)