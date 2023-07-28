import pandas as pd
import re

from classificadores.ClassificadorBase import ClassificadorBase
from util.RegexUtil import RegexUtil
import csv
import os.path
import subprocess


class ClassificaTRF01Acordaos(ClassificadorBase):

    def __init__(self, filename="acordaos"):

        novas_colunas = ['apela_parc_acolhida', 'apela_rejeit', 'apela_acolhida',
                         'agrav_parc_acolhidos','agravo_rejeit','agrav_acolhido',
                         'provido_parcial', 'negado', 'provido',
                         'embargo_parcial_acolhido','embargo_rejeitado', 'embargo_acolhido',
                         'sem_merito']

        super(ClassificaTRF01Acordaos, self).__init__(filename, novas_colunas)

    def trunca_texto_classificado(self, i, j, chunk, index, c):
        # trunca o texto para diminuir o arquivo de saída
        if i >= 0 and j > i:
            chunk.at[index, 'texto_movimento'] = c['texto_movimento'][i - 50: j + 50]

    def classifica_pelo_texto(self, chunk, index, c, classe):

        try:
            m = re.search(RegexUtil.txt_mov_recurso[classe], c['texto_movimento'])
        except Exception  as e:
            print(classe)
            raise e

        if m:
            i, j = m.span()
            chunk.at[index, classe] = 1
            self.trunca_texto_classificado(i, j, chunk, index, c)

            return True

        return False

    def classifica_pelo_tipo_movimento(self, chunk, index, c, classe):
        if re.search(RegexUtil.tp_mov_recurso[classe], c['tipo_movimento']):
            chunk.at[index, classe] = 1
            # chunk.at[index, 'texto_movimento'] = "[classificado pelo tipo movimento]"
            return True

        return False

    def classifica(self, chunk, index, c):

        # classificar de acordo com o tipo movimento do recurso
        for classe in ['provido_parcial', 'negado', 'provido']:
            if self.classifica_pelo_tipo_movimento(chunk, index, c, classe):
                self.por_tp += 1
                break
        for classe in ['embargo_parcial_acolhido','embargo_rejeitado', 'embargo_acolhido']:
            if self.classifica_pelo_tipo_movimento(chunk, index, c, classe):
                self.por_tp += 1
                break

        for classe in ['apela_parc_acolhida', 'apela_rejeit', 'apela_acolhida']:
            if self.classifica_pelo_tipo_movimento(chunk, index, c, classe):
                self.por_tp += 1
                break
        for classe in ['agrav_parc_acolhidos', 'agravo_rejeit', 'agrav_acolhido']:
            if self.classifica_pelo_tipo_movimento(chunk, index, c, classe):
                self.por_tp += 1
                break

        if self.classifica_pelo_tipo_movimento(chunk, index, c, 'sem_merito'):
            self.por_tp += 1

        # caso nao tenha sido possível classificar de acordo com o tipo da sentenca somente,
        # classificar de acordo com o texto da sentenca
        for classe in ['provido_parcial', 'negado', 'provido']:
            if self.classifica_pelo_texto(chunk, index, c, classe):
                self.por_txt += 1
                break

        for classe in ['embargo_parcial_acolhido','embargo_rejeitado', 'embargo_acolhido']:
            if self.classifica_pelo_texto(chunk, index, c, classe):
                self.por_txt += 1
                break

        if self.classifica_pelo_texto(chunk, index, c, 'sem_merito'):
            self.por_txt += 1

        ''' Não acredito que possa ter isso mais. pode ter mais de 1 sentença no mesmo texto.
        if c['provido_parcial'] + c['negado'] + c['provido'] + c['embargo_acolhido'] + c['embargo_rejeitado'] + c['embargo_parcial_acolhido'] > 1:
            import sys
            print('erro de classificacao dupla')
            sys.exit(0)'''
        return chunk

    def salva(self, chunk, write_header):

        nao_classificados = chunk[
            (chunk.provido_parcial == 0) & (chunk.negado == 0) & (chunk.provido == 0) & (chunk.embargo_acolhido == 0) & (chunk.embargo_rejeitado == 0) & (chunk.embargo_parcial_acolhido == 0) &
            (chunk.apela_parc_acolhida == 0) & (chunk.apela_rejeit == 0) & (chunk.apela_acolhida == 0) & (chunk.agrav_parc_acolhidos == 0) & (chunk.agravo_rejeit == 0) & (chunk.agrav_acolhido == 0)
            & (chunk.sem_merito == 0)]

        classificados = chunk[
            (chunk.provido_parcial == 1) | (chunk.negado == 1) | (chunk.provido == 1) | (chunk.embargo_acolhido == 1) |
            (chunk.embargo_rejeitado == 1) | (chunk.embargo_parcial_acolhido == 1) | (chunk.apela_parc_acolhida == 1) |
            (chunk.apela_rejeit == 1) |(chunk.apela_acolhida == 1) | (chunk.agrav_parc_acolhidos == 1) |
            (chunk.agravo_rejeit == 1) | (chunk.agrav_acolhido == 1) | (chunk.sem_merito == 1)]

        classificados.to_csv(self.filename.replace('.csv', '') + "-classificadas.csv", sep='\t', encoding='utf-8', mode='a',
                             header=write_header, index=False, quoting=csv.QUOTE_ALL, quotechar='"')
        nao_classificados.to_csv(self.filename.replace('.csv', '') + "-nao-classificadas.csv", sep='\t', encoding='utf-8',
                                 mode='a', header=write_header, index=False, quoting=csv.QUOTE_ALL, quotechar='"')


if __name__ == '__main__':

    # inicializa o classificador
    classificador = ClassificaTRF01Acordaos('reports/out/IMPROBIDADE_TRF4/tmp-acordaos.csv')
    classificador.run()
