# -*- coding:utf-8 -*-
import sys
import pandas as pd
import nltk
import datetime
from datetime import date
from pandas.core.algorithms import duplicated
from nltk.tokenize import word_tokenize
import matplotlib.pyplot as plt
import numpy as np
import random
import math
nltk.download('punkt')

dado_FatoFake = pd.DataFrame(columns=['link','titulo','categoria','data','texto'])
dado_Efarsas = pd.DataFrame(columns=['link','titulo','categoria','data','texto'])

#count = 0

def filtragemTexto(dataframe,destino):
    textos_filtrados = []
    textos_filtrados_total = []
    for i in range(0,len(dataframe)):
        texto = word_tokenize(dataframe.iloc[i]['texto'])
        tokens_without_sw = [word for word in texto if not word in words]
        textos_filtrados.append(tokens_without_sw)
        for token in tokens_without_sw:
            if(not token.isdigit()):
                textos_filtrados_total.append(token.lower())
                
    dataframe['texto'] = textos_filtrados
    if (destino):
        dataframe.to_csv(destino,index=False)
    return textos_filtrados_total

def contagemPalavras(dados,destino):
    if type(dados) == 'DataFrame':
        dados = dados['texto'].to_list()
        
    dados = pd.DataFrame(dados,columns=['palavras'])
    dados['repeticoes'] = dados['palavras'].map(dados['palavras'].value_counts())
    dados.sort_values(by=['repeticoes'],inplace=True,ascending=False)
    dados = dados.drop_duplicates()
    if destino:
        dados.to_csv(destino,index=False)
    else:
        return dados

def definir_periodo(dataframe, data_1, data_2):
    dataframe = dataframe[(dataframe['data'] > data_1) & (dataframe['data'] < str(data_2))]
    return dataframe

def converter_data(data):
    data = data.split('-')
    data = data[2]+"-"+data[1]+"-"+data[0]
    return data

def gera_grafico(dataframe,palavra):
    dataframe['data'] = pd.to_datetime(dataframe['data'])
    weeks = [g for n, g in dataframe.groupby(pd.Grouper(key='data',freq='W'))]

    frequencia = 0
    y = []
    x = []
    i = 0

    #estilo do grafico
    plt.style.use('fivethirtyeight')
    plt.xticks(fontsize = 8, rotation=90)

    #var para setar primeira e ultima data
    first_date = weeks[0]
    last_date = weeks[len(weeks)-1]

    for week in weeks:

        texto_filtrados_total = filtragemTexto(week,None)
        df = contagemPalavras(texto_filtrados_total,None)
        frequencia = df.loc[df.palavras == palavra,'repeticoes']

        if (not frequencia.empty):
            y.append(frequencia.iloc[0])
        else:
            y.append(0)
        
        try:
            x.append(str(week.iloc[0]['data'].date()))
        except:
            x.append(str(i))

        i = i+1

    ar = {'semana':x,'repeticoes':y}
    
    newDF = pd.DataFrame(ar)
    newDF.to_csv("repeticao_semana.csv",index=False)
    resumo_amostral(newDF,'resumo_amostral_por_semana.csv')
    #SISTEMA PARA CORES ALEATORIAS
    colors =["#ff0400","#0400ff","#00ff04","#ff0400","#ff8400","#ff007b","#00fbff","#fbff00","#ff00d0","#03ffc8","#26deff","#a04cff","#ff8a67","#86ff9c","#ff86e9","#ff9c86","#86e9ff","#86ff9c","#31c5ff","#fffc40"]
    rand_color = colors[random.randint(0, 20)]

    plt.bar(x, y, width=0.5, color=rand_color, label= palavra)
    plt.ylabel('frequencia')
    plt.xlabel('semanas')

    plt.title('ultima palavra chave: ' + palavra + ' (' + str(first_date.iloc[0]['data'].date()) + ' - ' + str(last_date.iloc[len(last_date)-1]['data'].date()) + ')')
    plt.legend()
    plt.tight_layout()
    plt.show()
    
    plt.savefig('graficosemana.png')

def resumo_amostral(dataframe,path_csv):
    #dataframe do describe
    describe_df = dataframe['repeticoes'].describe(include='all')

    #"scrape" das variaveis do describe
    num = describe_df.loc['count']
    media = describe_df.loc['mean']
    desvio = describe_df.loc['std']
    menor = describe_df.loc['min']
    q1 = describe_df.loc['25%']
    q2 = describe_df.loc['50%']
    q3 = describe_df.loc['75%']
    maior = describe_df.loc['max']
    #--- criacao das nossas variaveis ---
    mediana = 0
    if(num%2 != 0): 
        mediana = dataframe['repeticoes'].iloc[math.ceil(num/2)]
    else:
        p = (num+1)/2
        mediana = ( dataframe['repeticoes'].iloc[math.floor(p)] + dataframe['repeticoes'].iloc[math.ceil(p)] )/2
    
    modaMaior = 0
    for i in range(0,dataframe.__len__()):
        if dataframe['repeticoes'].iloc[modaMaior] < dataframe['repeticoes'].iloc[i]:
            modaMaior = i
            
    variancia = pow(desvio, 2)
    cv = desvio/media
    amplitude = maior - menor
    iq = (q3/4) - (q1/4)
    # -------
    try:
        data = {'estatisticas':['amostras', 'media', 'mediana', 'moda', 'desvio', 'variancia', 'cv', 'minimo', 'q1', 'q2', 'q3', 'maximo', 'iq', 'amplitude'], 'resultados':[num, media, mediana, dataframe['semana'].iloc[modaMaior], desvio, variancia, cv, menor, q1, q2, q3, maior, iq, amplitude]}
    except:
        data = {'estatisticas':['amostras', 'media', 'mediana', 'moda', 'desvio', 'variancia', 'cv', 'minimo', 'q1', 'q2', 'q3', 'maximo', 'iq', 'amplitude'], 'resultados':[num, media, mediana, dataframe['repeticoes'].iloc[0], desvio, variancia, cv, menor, q1, q2, q3, maior, iq, amplitude]}

    df = pd.DataFrame(data)

    df.to_csv(path_csv,index=False) #seria legal abrir um menu de "salvar em"

# todo
def analise_amostra(df):
    analise = pd.DataFrame(columns=["estatistica","analise"])
    # amostras int
    df['resultados'].iloc[0]

    #media float
    df['resultados'].iloc[1]

    #mediana int
    df['resultados'].iloc[2]

    #moda date
    df['resultados'].iloc[3]

    #desvio float
    df['resultados'].iloc[4]

    #variancia float
    df['resultados'].iloc[5]

    #coef. variacao float
    df['resultados'].iloc[6]
    
    #minimo int
    df['resultados'].iloc[7]

    #q1
    df['resultados'].iloc[8]

    #q2
    df['resultados'].iloc[9]

    #q3
    df['resultados'].iloc[10]

    #maximo
    df['resultados'].iloc[11]

    #iq
    df['resultados'].iloc[12]

    #amplitude
    df['resultados'].iloc[13]
    return

words = ['e.', 'Com','97305-9827','s??o','texto','+55','mostra','Circula','E','gente','Ela','Ele','informa????es','Foto','V??deo','uso','G1','Em',"#","%",'mensagem',"''",'Estava','Na','Conclus??o','informou','mostrando','ocorridos','frequentemente','v??deo','foto','site','Sim','N??o','Ser??','Em','``',';','//www.youtube.com/watch','S??','???','!',':','As',',','O','Os','A','???','???',"'",'(',')','.','?','Um','por','No','"','??','De','No','https','Atualiza????o','-','???','Publicidade','a', '??', 'adeus', 'agora', 'a??', 'ainda', 'al??m', 'algo', 'algu??m', 'algum', 'alguma', 'algumas', 'alguns', 'ali', 'ampla', 'amplas', 'amplo', 'amplos', 'ano', 'anos', 'ante', 'antes', 'ao', 'aos', 'apenas', 'apoio', 'ap??s', 'aquela', 'aquelas', 'aquele', 'aqueles', 'aqui', 'aquilo', '??rea', 'as', '??s', 'assim', 'at??', 'atr??s', 'atrav??s', 'baixo', 'bastante', 'bem', 'boa', 'boas', 'bom', 'bons', 'breve', 'c??', 'cada', 'catorze', 'cedo', 'cento', 'certamente', 'certeza', 'cima', 'cinco', 'coisa', 'coisas', 'com', 'como', 'conselho', 'contra', 'contudo', 'custa', 'da', 'd??', 'd??o', 'daquela', 'daquelas', 'daquele', 'daqueles', 'dar', 'das', 'de', 'debaixo', 'dela', 'delas', 'dele', 'deles', 'demais', 'dentro', 'depois', 'desde', 'dessa', 'dessas', 'desse', 'desses', 'desta', 'destas', 'deste', 'destes', 'deve', 'devem', 'devendo', 'dever', 'dever??', 'dever??o', 'deveria', 'deveriam', 'devia', 'deviam', 'dez', 'dezanove', 'dezasseis', 'dezassete', 'dezoito', 'dia', 'diante', 'disse', 'disso', 'disto', 'dito', 'diz', 'dizem', 'dizer', 'do', 'dois', 'dos', 'doze', 'duas', 'd??vida', 'e', '??', 'ela', 'elas', 'ele', 'eles', 'em', 'embora', 'enquanto', 'entre', 'era', 'eram', '??ramos', '??s', 'essa', 'essas', 'esse', 'esses', 'esta', 'est??', 'estamos', 'est??o', 'estar', 'estas', 'est??s', 'estava', 'estavam', 'est??vamos', 'este', 'esteja', 'estejam', 'estejamos', 'estes', 'esteve', 'estive', 'estivemos', 'estiver', 'estivera', 'estiveram', 'estiv??ramos', 'estiverem', 'estivermos', 'estivesse', 'estivessem', 'estiv??ssemos', 'estiveste', 'estivestes', 'estou', 'etc', 'eu', 'exemplo', 'fa??o', 'falta', 'favor', 'faz', 'fazeis', 'fazem', 'fazemos', 'fazendo', 'fazer', 'fazes', 'feita', 'feitas', 'feito', 'feitos', 'fez', 'fim', 'final', 'foi', 'fomos', 'for', 'fora', 'foram', 'f??ramos', 'forem', 'forma', 'formos', 'fosse', 'fossem', 'f??ssemos', 'foste', 'fostes', 'fui', 'geral', 'grande', 'grandes', 'grupo', 'h??', 'haja', 'hajam', 'hajamos', 'h??o', 'havemos', 'havia', 'hei', 'hoje', 'hora', 'horas', 'houve', 'houvemos', 'houver', 'houvera', 'houver??', 'houveram', 'houv??ramos', 'houver??o', 'houverei', 'houverem', 'houveremos', 'houveria', 'houveriam', 'houver??amos', 'houvermos', 'houvesse', 'houvessem', 'houv??ssemos', 'isso', 'isto', 'j??', 'la', 'l??', 'lado', 'lhe', 'lhes', 'lo', 'local', 'logo', 'longe', 'lugar', 'maior', 'maioria', 'mais', 'mal', 'mas', 'm??ximo', 'me', 'meio', 'menor', 'menos', 'm??s', 'meses', 'mesma', 'mesmas', 'mesmo', 'mesmos', 'meu', 'meus', 'mil', 'minha', 'minhas', 'momento', 'muita', 'muitas', 'muito', 'muitos', 'na', 'nada', 'n??o', 'naquela', 'naquelas', 'naquele', 'naqueles', 'nas', 'nem', 'nenhum', 'nenhuma', 'nessa', 'nessas', 'nesse', 'nesses', 'nesta', 'nestas', 'neste', 'nestes', 'ningu??m', 'n??vel', 'no', 'noite', 'nome', 'nos', 'n??s', 'nossa', 'nossas', 'nosso', 'nossos', 'nova', 'novas', 'nove', 'novo', 'novos', 'num', 'numa', 'n??mero', 'nunca', 'o', 'obra', 'obrigada', 'obrigado', 'oitava', 'oitavo', 'oito', 'onde', 'ontem', 'onze', 'os', 'ou', 'outra', 'outras', 'outro', 'outros', 'para', 'parece', 'parte', 'partir', 'paucas', 'pela', 'pelas', 'pelo', 'pelos', 'pequena', 'pequenas', 'pequeno', 'pequenos', 'per', 'perante', 'perto', 'pode', 'pude', 'p??de', 'podem', 'podendo', 'poder', 'poderia', 'poderiam', 'podia', 'podiam', 'p??e', 'p??em', 'pois', 'ponto', 'pontos', 'por', 'por??m', 'porque', 'porqu??', 'posi????o', 'poss??vel', 'possivelmente', 'posso', 'pouca', 'poucas', 'pouco', 'poucos', 'primeira', 'primeiras', 'primeiro', 'primeiros', 'pr??pria', 'pr??prias', 'pr??prio', 'pr??prios', 'pr??xima', 'pr??ximas', 'pr??ximo', 'pr??ximos', 'pude', 'puderam', 'quais', 'qu??is', 'qual', 'quando', 'quanto', 'quantos', 'quarta', 'quarto', 'quatro', 'que', 'qu??', 'quem', 'quer', 'quereis', 'querem', 'queremas', 'queres', 'quero', 'quest??o', 'quinta', 'quinto', 'quinze', 'rela????o', 'sabe', 'sabem', 's??o', 'se', 'segunda', 'segundo', 'sei', 'seis', 'seja', 'sejam', 'sejamos', 'sem', 'sempre', 'sendo', 'ser', 'ser??', 'ser??o', 'serei', 'seremos', 'seria', 'seriam', 'ser??amos', 'sete', 's??tima', 's??timo', 'seu', 'seus', 'sexta', 'sexto', 'si', 'sido', 'sim', 'sistema', 's??', 'sob', 'sobre', 'sois', 'somos', 'sou', 'sua', 'suas', 'tal', 'talvez', 'tamb??m', 'tampouco', 'tanta', 'tantas', 'tanto', 't??o', 'tarde', 'te', 'tem', 't??m', 't??m', 'temos', 'tendes', 'tendo', 'tenha', 'tenham', 'tenhamos', 'tenho', 'tens', 'ter', 'ter??', 'ter??o', 'terceira', 'terceiro', 'terei', 'teremos', 'teria', 'teriam', 'ter??amos', 'teu', 'teus', 'teve', 'ti', 'tido', 'tinha', 'tinham', 't??nhamos', 'tive', 'tivemos', 'tiver', 'tivera', 'tiveram', 'tiv??ramos', 'tiverem', 'tivermos', 'tivesse', 'tivessem', 'tiv??ssemos', 'tiveste', 'tivestes', 'toda', 'todas', 'todavia', 'todo', 'todos', 'trabalho', 'tr??s', 'treze', 'tu', 'tua', 'tuas', 'tudo', '??ltima', '??ltimas', '??ltimo', '??ltimos', 'um', 'uma', 'umas', 'uns', 'vai', 'vais', 'v??o', 'v??rios', 'vem', 'v??m', 'vendo', 'vens', 'ver', 'vez', 'vezes', 'viagem', 'vindo', 'vinte', 'vir', 'voc??', 'voc??s', 'vos', 'v??s', 'vossa', 'vossas', 'vosso', 'vossos', 'zero', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '_' ]
def startFiltragem(efarsas,data1,data2,Texto): #"main"
    textos_filtrados_total = []
    # if len(sys.argv)==2:
    #     dado_FatoFake = definir_periodo(dado_FatoFake, converter_data(sys.argv[1]),date.today())
    #     dado_Efarsas = definir_periodo(dado_Efarsas, converter_data(sys.argv[1]),date.today())
    if (efarsas):
        dado_Efarsas = pd.read_csv("efarsas.csv")
        dado_Efarsas = definir_periodo(dado_Efarsas,data1,data2)
        gera_grafico(dado_Efarsas,Texto)
        textos_filtrados_total = filtragemTexto(dado_Efarsas,"efarsas_filtrado.csv")
        contagemPalavras(textos_filtrados_total,"efarsas_repeticoes.csv")
        resumo_amostral(pd.read_csv("efarsas_repeticoes.csv"),'resumo_amostral.csv')

    else:
        dado_FatoFake = pd.read_csv("fato_fake.csv")
        dado_Efarsas = definir_periodo(dado_FatoFake,data1,data2)
        gera_grafico(dado_Efarsas,Texto)
        textos_filtrados_total = filtragemTexto(dado_FatoFake,"fato_fake_filtrado.csv")
        contagemPalavras(textos_filtrados_total,"fato_fake_repeticoes.csv")
        resumo_amostral(pd.read_csv("fato_fake_repeticoes.csv"),'resumo_amostral.csv')
