# projetoProbabilidade  

### Modo de utilizar:  
-  Necessita de Python3 e Pip (https://pip.pypa.io/en/stable/installation/)

- Abra um terminal na pasta do projeto
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

- No termnial, digite py Compilador_Fake_News.py(Windows) ou python3 Compilador_Fake_News.py(Linux) 

### Sites usados:  
- https://www.e-farsas.com/  
- https://g1.globo.com/fato-ou-fake/    

### Dados a serem pegos:    
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
- limitar o site a pesquisar
