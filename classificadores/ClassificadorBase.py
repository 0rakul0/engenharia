import pandas as pd
import os.path
import subprocess
import abc
import sys
import csv

csv.field_size_limit(100000000)

class ClassificadorBase(metaclass=abc.ABCMeta):

    def __init__(self, filename, novas_colunas,apaga_arquivo_classificados=True):

        self.filename = filename

        if apaga_arquivo_classificados:
            a = open(filename.replace('.csv', '')+"-classificadas.csv", "w")  # só pra zerar o arquivo
            a.close()
            a = open(filename.replace('.csv', '')+"-nao-classificadas.csv", "w")  # só pra zerar o arquivo
            a.close()

        self.novas_colunas = novas_colunas

        self.gera_entrada(filename)

        self.por_tp = 0
        self.por_txt = 0

    def adiciona_colunas(self, chunk):

        for coluna in self.novas_colunas:
            chunk[coluna] = 0

    def classifica(self, chunk, index, c):
        raise NotImplementedError

    def itera_chunk(self, chunk):

        for index, c in chunk.iterrows():
            yield index, c

    def salva(self, chunk, write_header):
        raise NotImplementedError

    def gera_entrada(self, tipo):

        if not os.path.isfile(tipo):
            subprocess.call('psql -d diario_mining -h postgresql10-rj -U diario-mining < sql/consulta_'+tipo.strip('.csv')+'.sql',
                            shell=True)

        # print('sentencas.csv criado')

    def run(self,modifica_tipos_para_tipo_movimento=False):

        write_header = True

        for chunk in self.le_arquivo_para_dataframe(self.filename, adiciona_colunas=True):
                if modifica_tipos_para_tipo_movimento:
                    chunk = chunk.astype(
                        {'sem_merito': str, 'parcial_proc': str, 'improc': str, 'procedente': str, 'acordo': str,
                         'baixa_definitiva': str,
                         'citacao': str, 'liminar_indeferida': str, 'liminar_deferida_parcial': str,
                         'liminar_deferida': str,
                         'contestacao_apresentada': str, 'contestacao_nao_apresentada': str, 'defesa_previa': str,
                         'transito_em_julgado': str,
                         'suspensao_processo_civel': str, 'suspensao_processo_penal': str, 'sobrestamento': str,
                         'recurso_apelacao_interposta_reu'
                         : str, 'recurso_agravo_retido_interposto_reu': str,
                         'recurso_recurso_adesivo_interposto_reu': str,
                         'recurso_apelacao_interposta_autor'
                         : str, 'recurso_recurso_adesivo_interposto_autor': str,
                         'recurso_agravo_retido_interposto_autor': str,
                         'recurso_embargos_infringentes_apresentados': str, 'recurso_apelacao_interposta'
                         : str, 'agravo_de_instrumento_interposto': str,
                         'recurso_recurso_sentido_estrito_interposto': str,
                         'agravo_interno_interposto': str,
                         'recurso_agravo_de_instrumento_apresentado_comprovante_de_interposicao': str,
                         'embargos_de_declaracao_opostos'
                         : str, 'convertido_diligencia': str, 'emb_parc_acolhidos': str, 'emb_acolhidos': str,
                         'emb_rejeit': str, 'extincao_punibilidade': str, 'apela_rejeit': str,
                         'apela_acolhida': str, 'apela_parc_acolhida': str, 'agrav_acolhido': str, 'agravo_rejeit': str,
                         'agrav_parc_acolhidos': str,
                         'seguranca_concedida': str, 'seguranca_rejeit': str, 'seguranca_parc_conced': str})
                # itera nos chunks através de generators
                for index, c in self.itera_chunk(chunk):

                    # faz a classificacao de uma única sentença
                    chunk = self.classifica(chunk, index, c)

                # salva o chunk classificado, separando classificados de não classificados em arquivos
                self.salva(chunk, write_header)

                # cabeçalho contendo nomes das colunas deve ser escrito somente para o primeiro bloco de sentenças
                write_header = False

        print('por txt:', self.por_txt, 'por tp', self.por_tp)

    def le_arquivo_para_dataframe(self, filename, chunksize=10 ** 3, adiciona_colunas=False):

        count = 0
        arq = pd.read_csv(filename, sep='\t', chunksize=chunksize, error_bad_lines=False, warn_bad_lines=True, engine='python')
        for chunk in arq:

            count += 1
            print('bloco', count)


            # inicialica chunk
            if adiciona_colunas:
                self.adiciona_colunas(chunk)

            chunk = chunk.fillna('texto indisponível, provavelmente devido a pdf escaneado')

            yield chunk