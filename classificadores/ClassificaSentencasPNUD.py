import re
from util.RegexUtil import RegexUtil
import os.path
import subprocess
from classificadores.ClassificadorBase import ClassificadorBase
from pdjus.modelo.Movimento import Movimento
from pdjus.dal.MovimentoDao import MovimentoDao
import csv
from pdjus.service.ProcessoService import ProcessoService

class ClassificaPNUD(ClassificadorBase):

    def __init__(self, filename):

        novas_colunas = ['texto_sentenca','sem_merito', 'parcial_proc', 'improc', 'procedente', 'emb_acolhidos', 'emb_parc_acolhidos', 'emb_rejeit', 'acordo', 'prescricao','extincao',
                         'ressarcimento_dano','perda_de_bens_ou_valores','perda_cargo_emprego_funcao','direitos_politicos','inelegivel','multa', 'proibicao_contratar_poder_publico']

        super(ClassificaPNUD, self).__init__(filename, novas_colunas,apaga_arquivo_classificados=False)

    def classifica(self,chunk,index, c):
        map_tipo_e_sentencas = self.separa_sentencas_do_movimento(c['texto_movimento'])
        if map_tipo_e_sentencas:
            return self.classifica_sentencas(map_tipo_e_sentencas,chunk,index)
        return None

    def separa_sentencas_do_movimento(self, movimento_texto):
        if not movimento_texto:
            return None
        lista_sentencas = list()
        map_tipo_e_sentencas = None
        for tipo,regex in RegexUtil.txt_mov_sentenca.items():
            for match in re.finditer(regex, movimento_texto):
                lista_sentencas.append((tipo,match))
        lista_sentencas = list(set(lista_sentencas))
        lista_sentencas = sorted(lista_sentencas, key=lambda item: item[1].start())
        
        if len(lista_sentencas) != 0:
            map_tipo_e_sentencas = {}
            i=0
            while(i<len(lista_sentencas)):
                tipo_da_sentenca = lista_sentencas[i][0]
                fim_da_sentenca = lista_sentencas[i+1][1].start() if i+1<len(lista_sentencas) else None
                texto_sentenca = movimento_texto[lista_sentencas[i][1].start():fim_da_sentenca].strip() #dois matches no mesmo lugar
                removeu_da_lista = False
                for classe in ['acordo', 'emb_parc_acolhidos',
                               'emb_acolhidos', 'emb_rejeit', 'sem_merito', 'parcial_proc', 'improc', 'procedente', 'prescricao','extincao']:
                    removeu_da_lista = False
                    texto_antigo_da_posicao_anterior = None
                    match = re.search(RegexUtil.txt_mov_sentenca[classe], lista_sentencas[i][1].group()+ ' ' +texto_sentenca)
                    if match and classe != tipo_da_sentenca:
                        removeu_da_lista = True
                        texto_antigo_da_posicao_anterior = movimento_texto[lista_sentencas[i-1][1].start():lista_sentencas[i][1].start()].strip()
                        lista_sentencas.remove(lista_sentencas[i])
                        break
                    elif match:
                        break
                if not removeu_da_lista:
                    if tipo_da_sentenca in list(map_tipo_e_sentencas.keys()):
                        map_tipo_e_sentencas[tipo_da_sentenca].append(texto_sentenca)
                    else:
                        map_tipo_e_sentencas.update({tipo_da_sentenca: [texto_sentenca]})
                    i+=1
                elif i>0:
                    fim_da_sentenca = lista_sentencas[i][1].start() if i < len(lista_sentencas) else None
                    posicao_texto_antigo_no_map = map_tipo_e_sentencas[lista_sentencas[i-1][0]].index(texto_antigo_da_posicao_anterior)
                    map_tipo_e_sentencas[lista_sentencas[i - 1][0]][posicao_texto_antigo_no_map] = movimento_texto[lista_sentencas[i-1][1].start():fim_da_sentenca].strip()

        return map_tipo_e_sentencas

    def classifica_sentencas(self,map_tipo_e_sentencas, chunk,index):
        data_frame_novo = None
        data_frame_aux = chunk.loc[index:index].copy()

        for tipo,sentencas in map_tipo_e_sentencas.items():
            for sentenca in sentencas:
                data_frame = data_frame_aux.copy()
                data_frame[tipo] = 1
                data_frame['texto_sentenca'] = sentenca
                # if tipo in ('parcial_proc', 'procedente'):
                #     encontrou_parte = False
                if re.search(RegexUtil.txt_pena_sentenca_pnud['ressarcimento_dano'], sentenca) and not re.search(RegexUtil.txt_pena_sentenca_pnud['negar_ressarcimento_dano'], sentenca):
                    data_frame['ressarcimento_dano'] = 1
                    # print('TEVE RESSARCIMENTO')
                    # ressarcimento = 1

                if re.search(RegexUtil.txt_pena_sentenca_pnud['perda_de_bens_ou_valores'], sentenca) and not re.search(RegexUtil.txt_pena_sentenca_pnud['negar_perda_de_bens_ou_valores'], sentenca):
                    data_frame['perda_de_bens_ou_valores'] = 1
                    # print('TEVE PERDA DE BENS')
                    # perda_bens = 1

                if re.search(RegexUtil.txt_pena_sentenca_pnud['perda_cargo_emprego_funcao'],sentenca) and not re.search( RegexUtil.txt_pena_sentenca_pnud['negar_perda_cargo_emprego_funcao'], sentenca):
                    data_frame['perda_cargo_emprego_funcao'] = 1
                    # print('TEVE PERDA DE CARGO')
                    # perda_cargo = 1

                if re.search(RegexUtil.txt_pena_sentenca_pnud['direitos_politicos'],sentenca) and not re.search(RegexUtil.txt_pena_sentenca_pnud['negar_direitos_politicos'], sentenca):
                    data_frame['direitos_politicos'] = 1
                    # print('TEVE PERDA DE DIREITOS POLÍTICOS')
                    # perda_direitos_politicos = 1

                if re.search(RegexUtil.txt_pena_sentenca_pnud['inelegivel'],sentenca) and not re.search(RegexUtil.txt_pena_sentenca_pnud['negar_inelegivel'], sentenca):
                    data_frame['inelegivel'] = 1
                    # print('TEVE INELEGIBILIDADE')
                    # inelegibilidade= 1

                if re.search(RegexUtil.txt_pena_sentenca_pnud['multa'],sentenca) and not re.search(RegexUtil.txt_pena_sentenca_pnud['negar_multa'], sentenca):
                    data_frame['multa'] = 1
                    # print('TEVE MULTA')
                    # multa= 1

                if re.search(RegexUtil.txt_pena_sentenca_pnud['proibicao_contratar_poder_publico'],sentenca) and not re.search(RegexUtil.txt_pena_sentenca_pnud['negar_proibicao_contratar_poder_publico'], sentenca):
                    data_frame['proibicao_contratar_poder_publico'] = 1
                    # print('TEVE PROIBIÇÃO DE CONTRATAR O PODER PÚBLICO')
                    # contratar_poder_publico= 1

                    #ENCONTRAR REU TEM PROBLEMAS, COMO ACHAR QUE O MINISTERIO PUBLICO É REU.. SÓ SE IDENTIFICARMOS AS PARTES QUE PODEM SER RÉUS
                    # for parte in processo.partes:
                    #     if parte.nome in sentenca:
                    #         encontrou_parte = True
                    #         print('Sentença {} para {} com ressarcimento={}, bens={}, cargo={},direitos_politicos={},inelegibilidade={}, multa={}, contratar_poder_publico={}'.
                    #               format(tipo,parte.nome,ressarcimento,perda_bens,perda_cargo,perda_direitos_politicos,inelegibilidade,multa,contratar_poder_publico))
                    # if not encontrou_parte:
                    #     print(
                    #         'Sentença {} sem identificar reu com ressarcimento={}, bens={}, cargo={},direitos_politicos={},inelegibilidade={}, multa={}, contratar_poder_publico={}'.
                    #         format(tipo, ressarcimento, perda_bens, perda_cargo, perda_direitos_politicos,
                    #                inelegibilidade, multa, contratar_poder_publico))
                if data_frame_novo is None:
                    data_frame_novo = data_frame.copy()
                else:
                    data_frame_novo = data_frame_novo.append(data_frame)
                # else:
                #     print(tipo)
                    #ENCONTRAR REU TEM PROBLEMAS, COMO ACHAR QUE O MINISTERIO PUBLICO É REU.. SÓ SE IDENTIFICARMOS AS PARTES QUE PODEM SER RÉUS
                    # encontrou_parte = False
                    # partes = list(set([p.nome for p in processo.partes]))
                    # for parte in partes:
                    #     if parte in sentenca:
                    #         encontrou_parte = True
                    #         print('Sentença {} para {}'.format(tipo, parte))
                    # if not encontrou_parte:
                    #     print('Sentença {} sem indentificar reu'.format(tipo))
        return data_frame_novo


    def run(self):

        write_header = True
        chunk_novo = None

        for chunk in self.le_arquivo_para_dataframe(self.filename, adiciona_colunas=True):

                # itera nos chunks através de generators
                for index, c in self.itera_chunk(chunk):

                    # faz a classificacao de uma única sentença
                    chunk_retorno = self.classifica(chunk, index, c)
                    if chunk_retorno is not None and not chunk_retorno.empty:
                        if chunk_novo is None or chunk_novo.empty:
                            chunk_novo= chunk_retorno
                        else:
                            chunk_novo = chunk_novo.append(chunk_retorno,ignore_index=True)

                if chunk_novo is not None and not chunk_novo.empty:
                    # salva o chunk classificado, separando classificados de não classificados em arquivos
                    self.salva(chunk_novo, write_header)
                    # cabeçalho contendo nomes das colunas deve ser escrito somente para o primeiro bloco de sentenças
                    write_header = False
                    chunk_novo = None

        print('por txt:', self.por_txt, 'por tp', self.por_tp)

    def salva(self, chunk, write_header):
        sentencas_classificadas = chunk[
                (chunk.emb_acolhidos == 1) | (chunk.parcial_proc == 1) | (chunk.emb_rejeit == 1) | (chunk.procedente == 1) | (
                        chunk.sem_merito == 1) | (chunk.improc == 1) | (chunk.acordo == 1) | (chunk.prescricao == 1) | (chunk.extincao == 1)]

        sentencas_nao_classificadas =  chunk[
                (chunk.emb_acolhidos == 0) & (chunk.parcial_proc == 0) & (chunk.emb_rejeit == 0) & (chunk.procedente == 0) & (
                        chunk.sem_merito == 0) & (chunk.improc == 0) & (chunk.acordo == 0) & (chunk.prescricao == 0) & (chunk.extincao == 0)]

        procedentes_classificados = chunk[((chunk.parcial_proc == 1) | (chunk.procedente == 1)) & (
                (chunk.ressarcimento_dano == 1) | (chunk.perda_de_bens_ou_valores == 1) | (
                    chunk.perda_cargo_emprego_funcao == 1)
                | (chunk.direitos_politicos == 1) | (chunk.inelegivel == 1) | (chunk.multa == 1) | (
                            chunk.proibicao_contratar_poder_publico == 1))]

        sentencas_classificadas_sem_penas = chunk[
            ((chunk.emb_acolhidos == 1) | (chunk.parcial_proc == 1) | (chunk.emb_rejeit == 1) | (
                        chunk.procedente == 1) | (
                    chunk.sem_merito == 1) | (chunk.improc == 1) | (chunk.acordo == 1) | (chunk.prescricao == 1) | (
                        chunk.extincao == 1))& ((chunk.ressarcimento_dano == 0) & (chunk.perda_de_bens_ou_valores == 0) & (chunk.perda_cargo_emprego_funcao == 0) &
                (chunk.direitos_politicos == 0) & (chunk.inelegivel == 0) & (chunk.multa == 0) & (chunk.proibicao_contratar_poder_publico == 0))]

        sentencas_classificadas.to_csv(self.filename.replace('.csv', '')+"-fatiadas-classificadas.csv",
                                           sep='\t', encoding='utf-8', mode='a', header=write_header, quoting=csv.QUOTE_ALL, quotechar='"', index=False)
        sentencas_nao_classificadas.to_csv(self.filename.replace('.csv', '')+"-fatiadas-nao-classificadas.csv",
                                           sep='\t', encoding='utf-8', mode='a', header=write_header, quoting=csv.QUOTE_ALL, quotechar='"', index=False)
        procedentes_classificados.to_csv(self.filename.replace('.csv', '')+"-fatiadas-procedentes-e-parciais-classificadas.csv",
                                           sep='\t', encoding='utf-8', mode='a', header=write_header, quoting=csv.QUOTE_ALL, quotechar='"', index=False)
        sentencas_classificadas_sem_penas.to_csv(self.filename.replace('.csv', '') + "-fatiadas-classificadas-sem-penas.csv",
               sep='\t', encoding='utf-8', mode='a', header=write_header, quoting=csv.QUOTE_ALL, quotechar='"',
               index=False)

        '''
        somente_penas_classificadas = chunk[((chunk.sem_merito == 0) & (chunk.improc == 0) &(chunk.parcial_proc == 0)&(chunk.procedente == 0))&
                                            ((chunk.ressarcimento_dano == 1) | (chunk.perda_de_bens_ou_valores == 1) | (chunk.perda_cargo_emprego_funcao == 1)
            | (chunk.direitos_politicos == 1) | (chunk.inelegivel == 1) | (chunk.multa == 1) | (chunk.proibicao_contratar_poder_publico == 1))]

        improcedentes_classificados = chunk[((chunk.sem_merito == 1) | (chunk.improc == 1))&
                                            ((chunk.ressarcimento_dano == 1) | (chunk.perda_de_bens_ou_valores == 1) | (chunk.perda_cargo_emprego_funcao == 1)
            | (chunk.direitos_politicos == 1) | (chunk.inelegivel == 1) | (chunk.multa == 1) | (chunk.proibicao_contratar_poder_publico == 1))]

        procedentes_classificados = chunk[((chunk.parcial_proc == 1)|(chunk.procedente == 1))& (
            (chunk.ressarcimento_dano == 1) | (chunk.perda_de_bens_ou_valores == 1) | (chunk.perda_cargo_emprego_funcao == 1)
            | (chunk.direitos_politicos == 1) | (chunk.inelegivel == 1) | (chunk.multa == 1) | (chunk.proibicao_contratar_poder_publico == 1))]

        procedentes_nao_classificados = chunk[((chunk.parcial_proc == 1)|(chunk.procedente == 1))&(chunk.ressarcimento_dano == 0) & (chunk.perda_de_bens_ou_valores == 0) & (chunk.perda_cargo_emprego_funcao == 0) &
                (chunk.direitos_politicos == 0) & (chunk.inelegivel == 0) & (chunk.multa == 0) & (chunk.proibicao_contratar_poder_publico == 0)]

        somente_penas_classificadas.to_csv(self.filename.replace('.csv', '')+"-somente-penas-classificadas.csv",
                                             sep='\t', encoding='utf-8', mode='a', header=write_header, quoting=csv.QUOTE_ALL, quotechar='"', index=False)

        improcedentes_classificados.to_csv(self.filename.replace('.csv', '')+"-improcedentes-sem-merito-penas-classificadas.csv",
                                           sep='\t', encoding='utf-8', mode='a', header=write_header, quoting=csv.QUOTE_ALL, quotechar='"', index=False)
        procedentes_classificados.to_csv(self.filename.replace('.csv', '')+"-procedentes-parc-penas-classificadas.csv",
                                         sep='\t', encoding='utf-8', mode='a', header=write_header, quoting=csv.QUOTE_ALL, quotechar='"', index=False)
        # procservice = ProcessoService()
        # for index, linha in self.itera_chunk(procedentes_nao_classificados):
        #     proc = procservice.dao.get_por_id(linha['processo_id'])
        #     if proc:
        #         print(proc.processo_principal_id)
        procedentes_nao_classificados.to_csv(self.filename.replace('.csv', '')+"-procedentes-parc-penas-nao-classificadas.csv",
                                             sep='\t', encoding='utf-8', mode='a', header=write_header, quoting=csv.QUOTE_ALL, quotechar='"', index=False)
'''

if __name__ == '__main__':
    cla = ClassificaPNUD('reports/out/PNUD_TRF2/tmp-sentencas.csv')
    cla.run()

    # movdao = MovimentoDao()
    # movimento = movdao.get_por_id(188610)
    # map_sentencas = cla.separa_sentencas_do_movimento(movimento)
    # cla.classifica_sentencas(map_sentencas, movimento.processo)