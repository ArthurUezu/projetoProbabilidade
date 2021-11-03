from pandas.core.algorithms import duplicated
import requests
import pandas as pd
from bs4 import BeautifulSoup

def tratamentoData(data):
    date = data.split(" de ")
    date[1] = mes_dicionario[date[1]]
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

def filtragemNoticia(noticia):
    texto = noticia.find_all('span')
    noticia = ""
    for paragrafo in texto:
        noticia = noticia +"\n"+ paragrafo.text
    return noticia

mes_dicionario = {'janeiro':1,'fevereiro':2,'março':3,'abril':4,'maio':5,'junho':6,'julho':7,'agosto':8,'setembro':9,'outubro':10,'novembro':11,'dezembro':12}
palavras_chave = ("corona", "coronavirus", "sars-cov-2", "covid") 

url_base = "https://www.e-farsas.com/page/"
url_final = "?s="

#lista para armazenar os dados recolhidos do site
dados = []

#loop principal do webscraper
for palavra in palavras_chave:
    pagina_atual=1
    paginas_total=2 #2 é apenas para inicializar a variável, o valor dela é alterado no próximo loop
    print('Palavra chave atual: ' + palavra)

    while pagina_atual != int(paginas_total) + 1:
        response_menu = requests.get(url_base+str(pagina_atual)+url_final+palavra) #site + palavra chave
        site_menu = BeautifulSoup(response_menu.text,'html.parser')
        container = site_menu.find('div', attrs={'class': 'td_block_inner tdb-block-inner td-fix-index'})
        noticias = container.find_all('div',attrs={'class':'td-module-meta-info'}) #recolhe cada box de noticia

        print("Pagina:",pagina_atual)
        #pega o numero de paginas total
        paginas_total = site_menu.find('span', attrs={'class': 'pages'})
        paginas_total = paginas_total.text.split(" de ")[1] #lista [pagina atual, pagina final
        
        #seleção das informações relevantes
        for noticia in noticias:
            data = noticia.find('time')
            data = tratamentoData(data.text)
            if int(data[2]) <= 2019:
                pagina_atual = int(paginas_total)
                break

            titulo = noticia.find('a',attrs={'rel':'bookmark'})
            print("Post: " + titulo.text)

            categoria = noticia.find('a',attrs={'class':'td-post-category'})
            categoria = filtragemCategoria(categoria)

            link_noticia = titulo['href']
            response_noticia = requests.get(link_noticia)
            site_noticia = BeautifulSoup(response_noticia.text,'html.parser')
            noticia_texto = site_noticia.find("div", attrs={"class": "td_block_wrap tdb_single_content tdi_99 td-pb-border-top td_block_template_1 td-post-content tagdiv-type"})
            noticia_texto = filtragemNoticia(noticia_texto)
            
            dados.append([link_noticia,titulo.text,categoria,data[0]+'/'+str(data[1])+'/'+data[2],noticia_texto]) #armazenamento dos dados na lista
        pagina_atual = pagina_atual + 1
        print('\n')

#remoção de dados duplicados
dados = pd.DataFrame(dados,columns=['link','titulo','categoria','data','texto']).drop_duplicates()
print(dados)

#armazenamento dos dados em csv
dados.to_csv("efarsas.csv",index=False)