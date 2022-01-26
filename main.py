from os import mkdir, sep
import requests
from bs4 import BeautifulSoup
import re

#abre o site e pega o conteudo 
soup = BeautifulSoup(requests.get("https://www.debit.com.br/tabelas/tabela-completa.php").text, "html.parser")

#seleciona as tabelas
tables = soup.select("table")

#compiladores para achar data e valor
data_compile = re.compile(r"\d\d.\d\d\d\d")
valor_compile = re.compile(r"\d?\d,\d\d")

#Dicionario contendo as Tabelas
tabelas = {}

for item in tables:
    #Pegas as datas e os valores no texto
    datas = data_compile.findall(str(item))
    valores = valor_compile.findall(str(item))
    if datas != []:
        meses = {}
        cont = 0
        #separa por ano e mes
        for data in datas:
            meses[data[0:2]] = valores[cont]        
            cont += 1

        tabelas[datas[cont-1][3:]] = meses

inflacoes = []
for i in range(10):
    #percorre cada ano da tabela
    for ano in tabelas:
        #percorre cada mês da tabela
        for mes in tabelas[ano]:
            #transfroma o valor ta tabela em float
            valor = float(tabelas[ano][mes].replace(",", "."))
            if len(inflacoes) != 0 and len(inflacoes) == 10:
                cont = 0
                #percorre cada valor da lista inflacoes e verifica qual o valor mais alto
                for value in inflacoes:
                    if valor > value[1]:
                        #Verifica se esse valor ja não tem na lista
                        if not (ano + "/" + mes ,valor) in inflacoes:
                            inflacoes[cont] = (ano + "/" + mes ,valor)
                    cont += 1
            #Adiciona os primeiros valores a lista
            elif len(inflacoes) < 10:
                inflacoes.append((ano + "/" + mes ,valor))
#Cria a pasta "Dados" caso ela não exista
try: mkdir("Dados")
except: pass

cont = 0
#Cria um arquivo com cada um dos dados da lista
for item in inflacoes:
    with open("Dados" + sep + f"{cont}_" + item[0].replace("/", "") + ".txt", "w") as arq:
        arq.write(f"Data: \t\t\t{item[0]}\n")
        arq.write(f"Porcentagem: \t{item[1]}%")
    cont += 1
