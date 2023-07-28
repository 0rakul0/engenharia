# -*- coding: utf-8 -*-

import pandas as pd
import re
from util.RegexUtil import RegexUtil
import csv
import os.path
import subprocess
from classificadores.ClassificadorBase import ClassificadorBase

class ClassificaTRF01Sentencas(ClassificadorBase):

    def __init__(self, filename="sentencas"):

        novas_colunas = ['acordo', 'emb_parc_acolhidos',
                       'emb_acolhidos', 'emb_rejeit', 'sem_merito', 'parcial_proc', 'improc', 'procedente', 'prescricao','extincao',
                         'classificado_tipo_movimento', 'classificado_texto_movimento']

        super(ClassificaTRF01Sentencas, self).__init__(filename, novas_colunas)


    def classifica_pelo_tipo_movimento(self, chunk, index, c, classe):

        if re.search(RegexUtil.tp_mov_sentenca[classe], c['tipo_movimento']):
            chunk.at[index, classe] = 1
            chunk.at[index,'classificado_tipo_movimento'] = 1
            # chunk.at[index, 'texto_movimento'] = "[classificado pelo tipo movimento]"
            self.por_tp += 1
            return True

        return False

    def trunca_texto_classificado(self, i, j, chunk, index, c):
        # trunca o texto para diminuir o arquivo de saída
        if i >= 0 and j > i:
            chunk.at[index, 'texto_movimento'] = c['texto_movimento'][max(i-50,0): min(j + 50, len(c['texto_movimento']))]

    def classifica_pelo_texto(self, chunk, index, c, classe):

        try:
            m = re.search(RegexUtil.txt_mov_sentenca[classe], c['texto_movimento'])
        except Exception  as e:
            print(classe)
            raise e

        if m:
            i, j = m.span()
            chunk.at[index, classe] = 1
            chunk.at[index, 'classificado_texto_movimento'] = 1
            self.trunca_texto_classificado(i, j, chunk, index, c)
            self.por_txt +=1
            return True

        return False

    def classifica(self, chunk, index, c):

        for classe in ['sem_merito', 'parcial_proc', 'improc', 'procedente', 'acordo']:
            if self.classifica_pelo_tipo_movimento(chunk, index, c, classe):
                return chunk


        # caso nao tenha sido possível classificar de acordo com o tipo da sentenca somente,
        # classificar de acordo com o texto da sentenca
        # else:

        for classe in ['acordo', 'emb_parc_acolhidos',
                       'emb_acolhidos', 'emb_rejeit', 'sem_merito', 'parcial_proc', 'improc', 'procedente', 'prescricao','extincao']:
            if self.classifica_pelo_texto(chunk, index, c, classe):
                return chunk

        if c['sem_merito'] + c['parcial_proc'] + c['improc'] + c['procedente'] + c['acordo'] + c[
            'emb_parc_acolhidos'] + c['emb_acolhidos'] + c['emb_rejeit'] > 1:
           # import sys
            print('erro de classificacao dupla')
           # sys.exit(0)
        return chunk


    def salva(self, chunk, write_header):

        #acordo	emb_parc_acolhidos	emb_acolhidos	emb_rejeit	sem_merito	parcial_proc	improc	procedente	prescricao	extincao


        nao_classificados = chunk[
                (chunk.emb_acolhidos == 0) & (chunk.emb_parc_acolhidos == 0) & (chunk.parcial_proc == 0) & (chunk.emb_rejeit == 0) & (chunk.procedente == 0) & (
                        chunk.sem_merito == 0) & (chunk.improc == 0) & (chunk.acordo == 0) & (chunk.prescricao == 0) & (chunk.extincao == 0)]

        classificados = chunk[
            (chunk.emb_acolhidos == 1) | (chunk.emb_parc_acolhidos == 1) | (chunk.parcial_proc == 1) | (chunk.emb_rejeit == 1) | (chunk.procedente == 1) | (
                    chunk.sem_merito == 1) | (chunk.improc == 1) | (chunk.acordo == 1) | (chunk.prescricao == 1) | (chunk.extincao == 1)]

        classificados.to_csv(self.filename.replace('.csv', '')+"-classificadas.csv", sep='\t', encoding='utf-8', mode='a', header=write_header, quoting=csv.QUOTE_ALL, quotechar='"', index=False)
        nao_classificados.to_csv(self.filename.replace('.csv', '')+"-nao-classificadas.csv", sep='\t', encoding='utf-8', mode='a', header=write_header, quoting=csv.QUOTE_ALL, quotechar='"', index=False)


if __name__ == '__main__':

    # inicializa o classificador
    classificador = ClassificaTRF01Sentencas('reports/out/IMPROBIDADE_TRF4/tmp-sentencas.csv')
    classificador.run()