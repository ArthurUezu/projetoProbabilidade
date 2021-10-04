from pandas.core.algorithms import duplicated
import requests
import pandas as pd
from bs4 import BeautifulSoup

def tratamentoData(data):
    date = data.split(" de ")
    date[1] = mes_dicionario[date[1]]
    return date

palavras_chave = ("corona", "coronavirus", "sars-cov-2", "covid") 

url_base = "https://www.e-farsas.com/page/"
url_final = "?s="
url_site = "https://www.e-farsas.com/page/1?s="

#lista para armazenar os dados recolhidos do site
dados = []
mes_dicionario = {'janeiro':1,'fevereiro':2,'março':3,'abril':4,'maio':5,'junho':6,'julho':7,'agosto':8,'setembro':9,'outubro':10,'novembro':11,'dezembro':12}


#loop principal do webscraper
for palavra in palavras_chave:
    data = [4,10,2021]
    j=13
    flag = True

    print('palavra chave atual: ' + palavra)

    while flag:
        response_menu = requests.get(url_base+str(j)+url_final+palavra) #site + palavra chave
        print("Pagina:",j)
        site_menu = BeautifulSoup(response_menu.text,'html.parser')
        noticias = site_menu.find_all('div',attrs={'class':'td-module-meta-info'}) #recolhe cada box de noticia

        #pega o numero de paginas total
        pag_total = site_menu.find('span', attrs={'class': 'pages'})
        pag_total_text = pag_total.text
        pag_total_text = pag_total_text.split(" de ") #lista [pagina atual, pagina final]


        #acaba o loop da palavra atual (quando acabar as paginas)
        if j == int(pag_total_text[1]):
            flag = False
            break

        #seleção das informações relevantes
        for i in range(0, 12):
            print("Post:",i)
            try:
                titulo = noticias[i].find('a',attrs={'rel':'bookmark'})
            except(IndexError):
                data[2]=0
                break
            data = noticias[i].find('time')
            data = tratamentoData(data.text)
            if(data=="2019"):
                flag = False
            categoria = noticias[i].find('a',attrs={'class':'td-post-category'})
            try:
                if(categoria.text=="Conspirações" or categoria.text=="Falso"):
                    categoria = "Falso"
                else:
                    categoria = "Verdadeiro"
            except(AttributeError):
                categoria = "Erro"
                continue
            link = titulo['href']
            response_post = requests.get(link)
            site_post = BeautifulSoup(response_post.text,'html.parser')
            noticia_texto = site_post.find("div", attrs={"class": "td_block_wrap tdb_single_content tdi_98 td-pb-border-top td_block_template_1 td-post-content tagdiv-type"})
            dados.append([link,titulo.text,categoria,data[0]+'/'+str(data[1])+'/'+data[2],noticia_texto.text]) #armazenamento dos dados na lista
        j = j + 1

#remoção de dados duplicados
dados = pd.DataFrame(dados,columns=['link','titulo','categoria','data','texto']).drop_duplicates()
print(dados)

#armazenamento dos dados em csv
dados.to_csv("efarsas.csv",index=False)