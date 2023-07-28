import time

import requests
from zeep import Client
from bs4 import BeautifulSoup
from util import StringUtil
from util import RegexUtil
from util.StringUtil import *
from pdjus.service.AssuntoService import AssuntoService

# client = Client(wsdl="https://www.cnj.jus.br/sgt/sgt_ws.php?wsdl")
# service = AssuntoService()
# for i in range(136,16000):
#     time.sleep(2)
#     if i % 10 == 0:
#         client = Client(wsdl="https://www.cnj.jus.br/sgt/sgt_ws.php?wsdl")
#     assunto = client.service.pesquisarItemPublicoWS('A',"C",i)
#     print(str(i))
#     if assunto:
#         assunto = assunto[0].nome
#         assunto = remove_varios_espacos(assunto.upper())
#         assunto = remove_acentos(assunto)
#         assunto = remove_caracteres_especiais(assunto)
#         assunto = re.sub('[,$;<>\/\-\:\!\+\_\=\@\#\%\(\)\[\]]', ' ', assunto)
#         assuntoobj = service.preenche_assunto(nome_assunto=assunto)
#         service.dao.salvar(assuntoobj)
#         print(assunto+": "+str(i))
#soup = BeautifulSoup(pagina.text)

s = requests.Session()
service = AssuntoService()
pagina = s.get("https://esaj.tjsp.jus.br/cjpg/assuntoTreeSelect.do?campoId=assunto&mostrarBotoesSelecaoRapida=true&conversationId=")
soup = BeautifulSoup(pagina.text)
matchesopen = soup.find_all("li", {'class': 'leafItem'})
matches_selectable = soup.find_all("span", {'class': 'node selectable checkable Unchecked'})
matches_not_selectable = soup.find_all("span", {'class': 'node checkable Unchecked'})
for matche in matchesopen:
    open = None
    try:
        open = matche.attrs["class"][1]
    except IndexError as e:
        pass
    if "ASSUNTOS ANTIGOS" not in matche.text:
        assunto = matche.text.strip().upper().replace('\n','')
        assunto = remove_acentos(assunto)
        assunto = re.sub('[,$;<>\/\-\:\!\+\_\=\@\#\%\(\)\[\]\.]', ' ', assunto)
        assunto = remove_varios_espacos(assunto)
        try:
            assuntoobj = service.preenche_assunto(nome_assunto=assunto)
        except Exception as e:
            print(e)
            continue
        try:
            service.dao.salvar(assuntoobj)
        except Exception as e:
            print(e)
        print(assunto)