# projetoProbabilidade  

### Modo de utilizar:  
-  Necessita de Python3 e Pip (https://pip.pypa.io/en/stable/installation/)
-  Instale os requisitos
  ```
  pip install -r requirements.txt
  ```
- Abra Compilador_Fake_News.py
- Para linux instale os requisitos acima e instale essas bibliotecas 
- Para ubuntu
```
sudo apt update && sudo apt  install libxcb-image0 libxcb-keysyms1 libxcb-render-util0 libxcb-xkb1 libxkbcommon-x11-0 libxcb-icccm4
```
- Para Arch
```
sudo pacman -Sy && sudo pacman -S libxcb-image0 libxcb-keysyms1 libxcb-render-util0 libxcb-xkb1 libxkbcommon-x11-0 libxcb-icccm4
```
- Ou instale com seu gerenciador de pacotes preferido.


### Sites usados:  
- https://www.e-farsas.com/  
- https://g1.globo.com/fato-ou-fake/    

### Visualização de dados:  
- Mapa de palavras  
- Frequencia de fake news de cada site  
- Diferença entre noticias verdadeiras e falsas?  

### Dados a serem pegos:  
Atenção! Salvem os dados nesta ordem:  
- link  
- titulo  
- categoria  
- data  
- texto  

### Ferramentas:  
- requests  
- pandas  
- matplot ou scilab  
- beautiful soup  
- NLTK  

### Features para o usuario:
- escolher palavras chave
- procurar uma noticia especifica
- escolher diferentes tipos de graficos
- limitar o site a pesquisar

### TODO LIST:  
- [ ] scraping lupa  ?
- [x] filtragem e tratamento de dados  
- [ ] visualização de dados  
- [ ] talvez fazer um arquivo em bash que roda tudo?
- [ ] implementar um novo sistema de indice que mostra meses/anos
- [x] fazer uma funcao na mao que mostre todas os atributos pedidos pela professora
- [x]adicionar mediana
- [x]adicionar moda
- [x]adicionar variancia
- [x]adicionar cv
- [x]adicionar amplitude
- [x]adicionar intervalo interquartil 
- [ ] SUGESTAO: quando salvar o resumo_estatistico.csv, pedir para o usuario salvar-lo em algum lugar

- [x] implementar relatorio de analise de dados
- [x] implementar um novo csv de instancias da palavra chave e a data(semana ou mes) em que elas aconteceram p/ criar grafico
