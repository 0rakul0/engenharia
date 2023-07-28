import csv
import re

from pdjus import dal
from pdjus.dal.AssuntoDao import AssuntoDao
from pdjus.service.AssuntoService import AssuntoService
from util.StringUtil import *


def criaregexassunto (assunto):
    regex = re.sub('[,$;<>\/\-\:\!\+\_\=\@\#\%\(\)\[\]]', ' ', assunto.nome)
    regex = re.sub(r'(DE\b)', r'(D[AEO]S)', remove_varios_espacos(regex))
    regex = regex.replace('AO','(AOS|OES|AES)')
    regex = re.sub(r'([AEIOU]\b)',r'\1S',remove_varios_espacos(regex))
    regex = re.sub(r'(S\b)',r'S?',regex)
    regex = re.sub(r'^|$',r"\\b",regex)
    regex = regex.replace(' ',r'\b\s*\b')
    return regex



if __name__ == '__main__':
    # with open('/home/b279950109/Downloads/assuntos_atuais.txt') as f:
    #     assuntos = f.readlines()
    #     service = AssuntoService()
    #     for assunto in assuntos:
    #         remove_varios_espacos(assunto)
    #         assunto.replace(' ',"")
    #         assunto = re.sub('\\n',"",assunto)
    #         assunto = assunto.strip().upper()
    #         assunto = remove_acentos(remove_caracteres_especiais(assunto))
    #         if not assunto == '':
    #             assunto =  re.sub('[,$;<>\/\-\:\!\+\_\=\@\#\%\(\)\[\]]', ' ', assunto)
    #             assuntoobj = service.preenche_assunto(nome_assunto=assunto)
    #             service.dao.salvar(assuntoobj)
    #             print(assunto)


    service = AssuntoService()
    assuntos = service.dao.listar()
    for assunto in assuntos:
        regex = criaregexassunto(assunto)
        with open('/home/b279950109/Downloads/regexassunto.csv', mode='a') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow([assunto.nome, regex])




    # with open('/home/b279950109/Downloads/regexassunto.csv', mode='r') as f:
    #     count = 0
    #     reader = csv.reader(f,delimiter=';',quoting=csv.QUOTE_NONE)
    #     linhas = list(reader)
    #     for id_objeto in linhas:
    #         id_objeto_corrigido = re.sub('[,$;<>\/\-\:\!\+\_\=\@\#\%\(\)\[\]]', ' ', id_objeto[0])
    #         match = re.search(id_objeto[1],remove_varios_espacos(id_objeto_corrigido))
    #         if not match:
    #             count = count +1
    #             print(remove_varios_espacos(id_objeto_corrigido)+':'+id_objeto[1])
    #     print(count)