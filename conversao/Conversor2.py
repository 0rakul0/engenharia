# -*- coding: utf-8 -*-

import os
from PyPDF2 import PdfFileReader
from util.FileManager import FileManager
from multiprocessing import current_process


class Conversor(object):

    def __init__(self, nome, filetype):
        self.__nome = nome
        self.__filetype = filetype
        self.__log = "log_conversao.txt"
        self.__erro = "erro_conversao.txt"

    def converte_diretorio(self):
        total = 0
        erros = 0
        fm = FileManager(self.__nome, self.__log)
        pendentes = fm.listar_datas_conversao_pendente(self.__filetype, converte_tudo=True)
        for data in pendentes:
            dir_entrada = fm.caminho(self.__filetype, data)
            dir_saida = fm.caminho("*.txt", data)
            if os.path.isdir(dir_entrada):
                for arq in sorted(os.listdir(dir_entrada), reverse=False):
                    nome_arq, ext = os.path.splitext(arq)
                    if ext.lower() == '.pdf':
                        if not os.path.isfile(os.path.join(dir_saida, nome_arq + ".txt")):
                            try:
                                self.converte_arquivo(os.path.join(dir_entrada, arq), os.path.join(dir_saida, nome_arq + ".txt"))
                                total += 1
                            except Exception as e:
                                erros += 1
                                print(f'Erro ao converter {arq}: {e}')
        print(f'Conversão de {total} PDFs concluída com {erros} erros.')

    def converte_arquivo(self, pdf_path, txt_path):
        print(f"Processo {current_process().name} convertendo arquivo {pdf_path}")
        try:
            # Converte o PDF para txt
            with open(pdf_path, "rb") as pdf_file:
                pdf_reader = PdfFileReader(pdf_file)
                text = ""
                for page in range(pdf_reader.getNumPages()):
                    text += pdf_reader.getPage(page).extractText()

            # Salva o texto em um novo arquivo txt
            with open(txt_path, "w", encoding="utf-8") as txt_file:
                txt_file.write(text)
        except Exception as e:
            print(f"Erro ao converter {pdf_path}: {str(e)}")
