from pdjus.dal.MovimentoDao import MovimentoDao
from pdjus.dal.MarcadorDao import MarcadorDao
from pdjus.dal.ProcessoDao import ProcessoDao
from pdjus.dal.ProcTempDao import ProcTempDao
from pdjus.dal.EmpresaDao import EmpresaDao
from pdjus.service.EmpresaService import EmpresaService
from pdjus.service.ParteProcessoService import ParteProcessoService
from pdjus.service.ParteService import ParteService
from util.StringUtil import remove_pontuacao, remove_caracteres_especiais
from datetime import datetime
from util.RegexUtil import RegexUtil
import pandas as pd
import numpy as np
import re
import os


class ClassificaEmpresaMovimento:
    def __init__(self):
        self.lista_tipo_parte_exclusao = ['SINDA',  'REPRTTEAT',  'DEPFITER',  'REPRESENTANTE LEGAL',  'ACUSADO',  'CURESP',  'INTERESDO',  'COMISS',  'ADMPASSIV',  'PROMOTTER',  'INTERESSADO',  'PROCDOR',  'TERINTCER',  'DEFENSOR COM OAB',  'AVALIADOR',  'ARREMTERC',  'REPRTATE',  'REPRESENTANTE',  'INDICIADO',  'ASSISTACUS',  'FLAGRANTEADO',  'ADVATIVO',  'ADMINISTRADOR',  'ADMATIVA',  'ALIMENTADO',  'CREDOR',  'INVENTARIANTE',  'CONJUGE',  'TERCEIRO',  'ADVOGADA',  'FALECIDO',  'ADVOGADO',  'MPF',  'GESTORA',  'ADVATIVA',  'ASSISTENTE',  'SINDICA',  'ADMINISTRADOR JUDICIAL',  'COMISSARIA',  'INTERESSADA',  'ADMATIVO',  'ADM-PASSIV',  'ADMTERC',  'PROCURADORA',  'HERDEIRA',  'MINISTERIO PUB',  'J. DPCTE',  'FIADTERC',  'PREPOSTO',  'REPRESENTANTE/NOTICIANTE',  'INTERESDA',  'MAE',  'REPRELEG',  'ALIMENTADA',  'ADV(ATIVO)',  'INTERSDOQUERLT',  'PROCURADOR',  'INVTANTE',  'GUARDIAO',  'UNIDADE EXTERNA',  'MINISTERIO PUBLICO FEDERAL',  'CURADOR',  'SINDICO',  'COMISSARIO',  'PERITO',  'AGENCIA DA PREVIDENCIA SOCIAL',  'ADV-PASSIV',  'CURADOR ESPECIAL',  'DEPOSITARIO',  'A. CURIAE',  'ADM-TERC.',  'INTERESDO.',  'ADM(ATIVO)',  'GESTOR',  'TERINTINC',  'HERDEIRO',  'ARREMATANTE',  'INTERESDA.',  'SOC. ADVOGADOS',  'FISCAL']
        #self.regex_def_proc = '(((\\bDETERMINO\s*\w.{0,50}|\\bDEF(?:IRO|ERINDO-SE|ERIU)\s*(?:A|O)?\s*(?:PEDIDO)?\s*(?:D[OEA]S?)?\s*)(?:PROCESSAMENTO)\s*(?:D[OEA]S?)?\s*(?:PRESENTE)?\s?(?:PEDIDO)?\s*(?:D[OEA]S?)?\s*(?:REC\.?(?:UPERACAO)?\s*JUD\.?(?:ICIAL)?|CONCORDATA)?)|(\\bDEF[EI]R(?:O|IU)[\,\s]+(EM\s*FAVOR\s*D[AEO]S?)?.{0,50}A?\sRECUPERACAO\sJUDICIAL)).*?(COMO\s*ADMINISTRADOR(?:A)?\s*JUDICIAL.{1,250}NOMEIO|NOMEIO\s*COMO\s*ADMINISTRADOR(?:A)?\s*JUDICIAL)'
        #self.regex_neg_def_proc = '((?:INDEF[EI]R(?:O|IU))\s*(?:A|O)?\s*(?:PEDIDO)?\s*(?:D[OEA]S?)?\s*(?:PROCESSAMENTO)\s*(?:D[OEA]S?)?\s*(?:PEDIDO)?\s*(?:D[OEA]S?)?\s*(?:REC\.?(?:UPERACAO)?\s*JUD\.?(?:ICIAL)?|CONCORDATA)?)|(INDEF[EI]R(?:O|IU)[\,\s]+(EM\s*FAVOR\s*D[AEO]S?)?.{0,50}A?\sRECUPERACAO\sJUDICIAL)'
        self.regex_adm_judicial = '.*(COMO\s*ADMINISTRADOR(?:A)?\s*JUDICIAL.{1,250}NOMEIO|NOMEIO\s*COMO\s*ADMINISTRADOR(?:A)?\s*JUDICIAL)'
        self.regex_numeracao_cnpj = '(\d{13,14}|\s*\d{2}\s*\.\s*\d{3}\s*\.\s*\d{3}\s*\/\s*\d{4}\s*\-\s*\d{2}\s*)'
        self.regex_cnpj = '(?:CNPJ(?:\s*(M[EF]\s*SOB\s*O?\s*)?NO?)?\s*)' + self.regex_numeracao_cnpj
        self.processodao = ProcessoDao()
        self.marcadordao = MarcadorDao()
        self.movimentodao = MovimentoDao()
        self.proctempdao = ProcTempDao()
        self.empresadao = EmpresaDao()
        self.parteprocessoservice = ParteProcessoService()
        self.parteservice = ParteService()
        self.empresa_service = EmpresaService()
        self.regex_util = RegexUtil()
        self.cnpjs_com_empresa = []
        self.cnpjs_encontrados = []

    def classifica_empresa_recuperanda(self, processo, movimento):

        lista_tpparte_nomeparte_cnpj = []
        partes_processo = list(processo.partes_processo)
        lista_id_texto_movimento = self.filtra_movimentos([movimento])

        if lista_id_texto_movimento == []:
            return None

        lista_tpparte_nomeparte = [(pp.tipo_parte.nome, pp.parte.nome) for pp in partes_processo]
        lista_tpparte_nomeparte_cnpj, mensagens = self.busca_empresa_cnpj_no_movimento(lista_tpparte_nomeparte, lista_id_texto_movimento, processo, lista_tpparte_nomeparte_cnpj)

        qtd_cnpj_sem_empresa_recuperanda = set(self.cnpjs_encontrados) - set(self.cnpjs_com_empresa)

        dicionario_movid_cnpj = {}
        if len(qtd_cnpj_sem_empresa_recuperanda) > 0:
            for tupla in qtd_cnpj_sem_empresa_recuperanda:
                dicionario_movid_cnpj.update({tupla[1]: tupla[0]})

            qtd_cnpj_sem_empresa_recuperanda = [(item[1], item[0]) for item in dicionario_movid_cnpj.items()]
            self.escreve_csv_npu_processoid_cnpj(qtd_cnpj_sem_empresa_recuperanda, processo)

        self.cnpjs_com_empresa = []
        self.cnpjs_encontrados = []

        [print(mensagem) for mensagem in sorted(mensagens)]

    def classifica_empresa_recuperanda_proc_temp(self, processo):

        processo = self.processodao.get_por_id(processo.numero)
        lista_tpparte_nomeparte_cnpj = []
        partes_processo = list(processo.partes_processo)
        lista_id_texto_movimento = [(mov.id, mov.texto) for mov in processo.movimentos]

        if lista_id_texto_movimento == []:
            return None

        lista_tpparte_nomeparte = [(pp.tipo_parte.nome, pp.parte.nome, pp.parte.id) for pp in partes_processo]
        lista_tpparte_nomeparte_cnpj, mensagens = self.busca_empresa_cnpj_no_movimento(lista_tpparte_nomeparte, lista_id_texto_movimento, processo, lista_tpparte_nomeparte_cnpj)

        mov_id_cnpjs_sem_empresa_recuperanda = set(self.cnpjs_encontrados) - set(self.cnpjs_com_empresa)

        dicionario_movid_cnpj = {}
        if len(mov_id_cnpjs_sem_empresa_recuperanda) > 0:
            for mov_id, cnpj in mov_id_cnpjs_sem_empresa_recuperanda:
                dicionario_movid_cnpj.update({cnpj: mov_id})

            mov_id_cnpjs_sem_empresa_recuperanda = [(id_mov, cnpj) for cnpj, id_mov in dicionario_movid_cnpj.items()]
            possiveis_partes_recuperandas = list(filter(lambda tp: tp[0] not in self.lista_tipo_parte_exclusao, lista_tpparte_nomeparte))
            lista_cnpjs_sem_match_no_banco_da_receita = self.busca_empresas_por_cnpj_no_banco_da_receita(mov_id_cnpjs_sem_empresa_recuperanda, possiveis_partes_recuperandas, processo)

            if len(lista_cnpjs_sem_match_no_banco_da_receita) > 0:
                self.escreve_csv_npu_processoid_cnpj(mov_id_cnpjs_sem_empresa_recuperanda, processo)

        self.cnpjs_com_empresa = []
        self.cnpjs_encontrados = []

        [print(mensagem) for mensagem in sorted(mensagens)]

    def busca_empresas_por_cnpj_no_banco_da_receita(self, mov_id_cnpjs_sem_empresa_recuperanda, possiveis_partes_recuperandas, processo):
        lista_tpparte_nomeparte_cnpj = []
        lista_cnpjs_sem_match_no_banco_da_receita = []

        for cnpj in mov_id_cnpjs_sem_empresa_recuperanda:
            empresas = self.empresadao.get_no_banco_da_receita_federal_por_cnpj(remove_pontuacao(str(cnpj[1])).replace(' ', ''))
            if empresas:
                for empresa in empresas:
                    matches_parte = list(filter(lambda nome: empresa['razao_social'] == nome[1], possiveis_partes_recuperandas))
                    if len(matches_parte) > 0:
                        [lista_tpparte_nomeparte_cnpj.append((tipo_parte[0], empresa['razao_social'], empresa['cnpj'])) for tipo_parte in matches_parte]
            else:
                lista_cnpjs_sem_match_no_banco_da_receita.append((cnpj[0], str(cnpj[1])))

        if len(lista_tpparte_nomeparte_cnpj) > 0:
            lista_tpparte_nomeparte_cnpj = list(set(lista_tpparte_nomeparte_cnpj))
            self.salva_parte_empresa_cnpj(processo, lista_tpparte_nomeparte_cnpj)
            self.salva_relacao_recuperanda_parte_processo(processo, lista_tpparte_nomeparte_cnpj)

        return lista_cnpjs_sem_match_no_banco_da_receita

    def filtra_movimento_marcador(self, rank=0, fatia=1, tag='FALENCIAS', dias=7, limit=None, random=True, distinct=False):

        movimentos = []
        for marcador in self.regex_util.regex_movimento_marcador:
            movimentos.extend(list(self.movimentodao.listar_movimentos_por_marcador(marcador[2].upper())))

        processos_ids = list(set([item.processo_id for item in movimentos]))
        print(f'Processos distintos filtrados por deferimento processamento encontrados: {len(processos_ids)}')

        for processo in processos_ids:
            processo = self.processodao.get_por_id(processo)
            lista_tpparte_nomeparte_cnpj = []
            partes_processo = list(processo.partes_processo)
            lista_id_texto_movimento = self.filtra_movimentos(list(processo.movimentos))

            if lista_id_texto_movimento == []:
                continue

            lista_tpparte_nomeparte = [(pp.tipo_parte.nome, pp.parte.nome) for pp in partes_processo]
            #tipo_parte_partes_filter = list(filter(lambda tp: tp[0] not in self.lista_tipo_parte_exclusao, lista_tpparte_nomeparte))
            lista_tpparte_nomeparte_cnpj, mensagens = self.busca_empresa_cnpj_no_movimento(lista_tpparte_nomeparte, lista_id_texto_movimento, processo, lista_tpparte_nomeparte_cnpj)

            qtd_cnpj_sem_empresa_recuperanda = set(self.cnpjs_encontrados) - set(self.cnpjs_com_empresa)

            dicionario_movid_cnpj = {}
            if len(qtd_cnpj_sem_empresa_recuperanda) > 0:
                for tupla in qtd_cnpj_sem_empresa_recuperanda:
                    dicionario_movid_cnpj.update({tupla[1]: tupla[0]})

                qtd_cnpj_sem_empresa_recuperanda = [(item[1], item[0]) for item in dicionario_movid_cnpj.items()]
                self.escreve_csv_npu_processoid_cnpj(qtd_cnpj_sem_empresa_recuperanda, processo)

            self.cnpjs_com_empresa = []
            self.cnpjs_encontrados = []

            [print(mensagem) for mensagem in sorted(mensagens)]


    def filtra_movimentos(self, movimentos):
        lista_id_texto_movimento = []

        for movimento in movimentos:
            for marcador in movimento.marcadores:
                if marcador.nome in [marc[2].upper() for marc in self.regex_util.regex_movimento_marcador]:
                    try:
                        #match_def_proc = re.search(self.regex_def_proc, movimento.texto).group(0)
                        if re.search('CNPJ', movimento.texto):
                            lista_id_texto_movimento.append((movimento.id, movimento.texto))
                    except Exception:
                        continue

        return lista_id_texto_movimento


    def filtra_movimentos_cnpj(self, movimentos):
        lista_id_texto_movimento = []

        for movimento in movimentos:
            try:
                if re.search('CNPJ', movimento.texto):
                    lista_id_texto_movimento.append((movimento.id, movimento.texto))
            except Exception:
                continue

        return lista_id_texto_movimento

    def filtra_movimentos_nome_partes(self, movimentos, partes):
        lista_id_texto_movimento = []
        partes = [pp.parte.nome for pp in partes]

        for movimento in movimentos:
            for parte in partes:
                try:
                    if re.search(remove_caracteres_especiais(parte), remove_caracteres_especiais(movimento.texto)):
                        lista_id_texto_movimento.append((movimento.id, movimento.texto))
                except Exception:
                    continue

        return lista_id_texto_movimento


    def busca_empresa_cnpj_no_movimento(self, lista_tpparte_nomeparte, lista_id_texto_movimento, processo, lista_tpparte_nomeparte_cnpj):
        mensagens = []
        lista_empresas_sem_cnpj = []

        for id_mov, texto_mov in lista_id_texto_movimento:
            cnpj = None
            empresa = None
            self.verifica_cnpj_movimento(texto_mov, id_mov)
            for id, partes in enumerate(lista_tpparte_nomeparte):
                tipo_parte = partes[0]
                nome_parte = partes[1]
                parte_id = partes[2]
                try:
                    cnpj = re.search(f'{remove_caracteres_especiais(nome_parte)}''.{0,100}?'f'{self.regex_cnpj}', remove_caracteres_especiais(texto_mov))
                except Exception as e:
                    if ('nothing to repeat at position 0' == e.__str__()) or ('bad escape (end of pattern) at position 0' == e.__str__()):
                        continue

                if cnpj is None:
                    try:
                        empresa = re.search(f'{remove_caracteres_especiais(nome_parte)}', remove_caracteres_especiais(texto_mov))
                    except Exception as e:
                        if ('nothing to repeat at position 0' == e.__str__()) or ('bad escape (end of pattern) at position 0' == e.__str__()):
                            continue

                    if empresa is None:
                        continue
                    else:
                        if tipo_parte not in self.lista_tipo_parte_exclusao:
                            partes_da_lista_exclusao = list(map(lambda nome_parte: nome_parte[1], list(filter(lambda tp: tp[0] in self.lista_tipo_parte_exclusao, lista_tpparte_nomeparte))))
                            if len(nome_parte) > 1 and nome_parte not in partes_da_lista_exclusao:
                                lista_empresas_sem_cnpj.append((tipo_parte, nome_parte, parte_id))
                        continue

                lista_temp = []
                lista_temp.extend(lista_tpparte_nomeparte)

                if len(lista_temp) > 1:
                    lista_temp.pop(id)

                lista_temp = list(set([remove_caracteres_especiais(item[1]) for item in lista_temp]))
                regex_partes = '|'.join(lista_temp).replace(' ', '\s*')

                match_empresas_sem_cnpj = re.search(regex_partes, re.sub(f'^{remove_caracteres_especiais(nome_parte)}', '', cnpj.group(0)))


                if match_empresas_sem_cnpj: # é uma empresa sem CNPJ e se não tivesse esse controle ele iria atribuir o cnpj a empresa errada
                    empresa_sem_cnpj = nome_parte
                    parte_empresa = list(filter(lambda prt: prt[1] == empresa_sem_cnpj, lista_tpparte_nomeparte))

                    for t_prt, nm_prt, prt_id in parte_empresa:
                        if t_prt not in self.lista_tipo_parte_exclusao:
                            lista_empresas_sem_cnpj.append((t_prt, nm_prt, prt_id))

                    continue

                cnpj = re.search(self.regex_numeracao_cnpj, cnpj.group(0)).group(0)
                self.cnpjs_com_empresa.append((texto_mov[0], cnpj))

                if nome_parte in texto_mov and (tipo_parte, nome_parte, cnpj) not in lista_tpparte_nomeparte_cnpj:
                    mensagem_asterico = '************************************************************************************'
                    mensagens.append(f'{mensagem_asterico}\n* Empresa: "{nome_parte}"\n* Inscrita no CNPJ: "{cnpj}"\n* Relacionada ao processo: {processo.npu_ou_num_processo}\n* Movimento de id: {id_mov}\n* Tipo parte: {tipo_parte}')
                    lista_tpparte_nomeparte_cnpj.append((tipo_parte, nome_parte, cnpj))


        #self.salva_parte_empresa_cnpj(processo, lista_tpparte_nomeparte_cnpj)

        lista_empresas_sem_cnpj = list(set(lista_empresas_sem_cnpj))

        lista_tpparte_nomeparte_cnpj.extend(lista_empresas_sem_cnpj)

        #self.salva_relacao_recuperanda_parte_processo(processo, lista_tpparte_nomeparte_cnpj)

        if len(lista_empresas_sem_cnpj) > 0:
            lista_empresas_sem_cnpj = list(set([(emp[1], emp[2]) for emp in lista_empresas_sem_cnpj]))
            self.busca_empresas_banco_da_receita(lista_empresas_sem_cnpj, processo)

        return lista_tpparte_nomeparte_cnpj, mensagens


    def busca_empresas_banco_da_receita(self, lista_empresas_sem_cnpj, processo):
        for empresa in lista_empresas_sem_cnpj:
            empresas = self.empresadao.get_no_banco_da_receita_federal_por_razao_social_ou_nome_fantasia(empresa[0])
            parte_id = empresa[1]
            nome_parte = empresa[0]
            if len(empresas) > 0:
                for emp in empresas:
                    cnpj = emp['cnpj']
                    razao_social = emp['razao_social']
                    nome_fantasia = emp['nome_fantasia']
                    print(f'Salvando a parte "{nome_parte}" vinda do banco da receita com o cnpj "{cnpj}" no arquivo - empresas_encontradas_no_banco_da_receita.csv')
                    self.salva_csv_parte_id_nome_parte_match_nome_receita_cnpjs(parte_id, nome_parte, razao_social, nome_fantasia, cnpj)
            else:
                print(f'Salvando a parte "{nome_parte}" que não deu match no banco da receita no arquivo - empresas_que_nao_foram_encontradas_no_banco_da_receita.csv')
                self.salva_csv_parte_id_nome_parte_sem_match_no_banco_da_receita(parte_id, nome_parte, processo.id)


    def salva_csv_parte_id_nome_parte_sem_match_no_banco_da_receita(self, parte_id, nome_parte, processo_id):
        primeira_rodada = False

        if not os.path.exists('../csvs/empresas_que_nao_foram_encontradas_no_banco_da_receita.csv'):
            primeira_rodada = True

        df = pd.DataFrame()

        df = df.append([[parte_id, nome_parte, processo_id]])

        if primeira_rodada:
            df.rename(columns={0: 'parte_id', 1: 'nome_parte', 2: 'processo_id'}, inplace=True)
            df.to_csv('../csvs/empresas_que_nao_foram_encontradas_no_banco_da_receita.csv', sep=';', mode='a+', header=True, index=False)
        else:
            df.to_csv('../csvs/empresas_que_nao_foram_encontradas_no_banco_da_receita.csv', sep=';', mode='a+', header=False, index=False)


    def salva_csv_parte_id_nome_parte_match_nome_receita_cnpjs(self, parte_id, nome_parte, razao_social, nome_fantasia, cnpj):
        primeira_rodada = False

        if not os.path.exists('../csvs/cnpjs_sem_match_de_nome_parte_e_nem_encontrados_na_receita.csv'):
            primeira_rodada = True

        df = pd.DataFrame()

        # df = df.append([[parte_id, nome_parte, razao_social, nome_fantasia, cnpj]])
        df = df.append([[parte_id, nome_parte, razao_social, cnpj]])

        if primeira_rodada:
            df.rename(columns={0: 'parte_id', 1: 'nome_parte', 2: 'nome_receita', 3: 'cnpj'}, inplace=True)
            # df.rename(columns={0: 'parte_id', 1: 'nome_parte', 2: 'nome_receita', 3: 'nome_fantasia', 4: 'cnpj'}, inplace=True)
            df.to_csv('../csvs/cnpjs_sem_match_de_nome_parte_e_nem_encontrados_na_receita.csv', sep=';', mode='a+', header=True, index=False)
        else:
            df.to_csv('../csvs/cnpjs_sem_match_de_nome_parte_e_nem_encontrados_na_receita.csv', sep=';', mode='a+', header=False, index=False)


    def verifica_cnpj_movimento(self, texto_mov, id_mov):
        movimento_cropado = None
        cnpjs = None
        movimento_nulo = False

        if texto_mov is not None:
            movimento_cropado = re.search(self.regex_adm_judicial, texto_mov)
        else:
            movimento_nulo = True

        if movimento_cropado:
            cnpjs = re.findall(self.regex_cnpj, movimento_cropado.group(0))
        elif movimento_nulo is False:
            cnpjs = re.findall(self.regex_cnpj, texto_mov)

        if cnpjs:
            [self.cnpjs_encontrados.append((id_mov, cnpj[1])) for cnpj in cnpjs]

    def escreve_csv_npu_processoid_cnpj(self, mov_id_cnpjs_sem_empresa_recuperanda, processo):
        primeira_rodada = False

        if not os.path.exists('../csvs/cnpjs_nao_classificados_distintos_producao_v2.csv'):
            primeira_rodada = True

        df = pd.DataFrame()

        for movimento_id, cnpj in mov_id_cnpjs_sem_empresa_recuperanda:
            df = df.append([[str(processo.id), str(movimento_id), str(processo.npu_ou_num_processo), str(cnpj)]])

        if primeira_rodada:
            df.rename(columns={0: 'processo_id', 1: 'movimento_id', 2: 'NPU', 3: 'CNPJ'}, inplace=True)
            df.to_csv('../csvs/cnpjs_nao_classificados_distintos_producao_v2.csv', sep=';', mode='a+', header=True, index=False)
        else:
            df.to_csv('../csvs/cnpjs_nao_classificados_distintos_producao_v2.csv', sep=';', mode='a+', header=False, index=False)

    def salva_parte_empresa_cnpj(self, processo, lista_tpparte_nomeparte_cnpj):
        for tipo_parte, nome_parte, cnpj in lista_tpparte_nomeparte_cnpj:
            empresa = self.empresa_service.preenche_empresa(cnpj, nome_parte)
            for parte in processo.partes:
                if parte.nome == nome_parte:
                    parte.empresa = empresa
                    self.parteservice.dao.salvar(parte)

    def salva_relacao_recuperanda_parte_processo(self, processo, lista_tpparte_nomeparte_cnpj):
        for partes in lista_tpparte_nomeparte_cnpj:
            if remove_pontuacao(partes[0]) in self.lista_tipo_parte_exclusao:
                continue
            for parte in processo.partes:
                try:
                    if parte.nome == partes[1]:
                        parte_processo = self.parteprocessoservice.dao.get_por_parte_parte_processo(processo, parte)
                        if parte_processo.tipo_parte.nome == partes[0]:
                            parte_processo.recuperanda = True
                            self.parteprocessoservice.salvar(parte_processo)
                except Exception as e:
                    print(e)


# if __name__ == '__main__':
#     c = ClassificaEmpresaMovimento()
#
#     # data = pd.read_csv('/home/e7609043/PycharmProjects/IpeaJUS/csvs/cnpjs_nao_classificados_distintos_producao.csv', sep=';')
#     # print()
#
#     rank = 4
#     fatia = 5
#
#     print(f'RANK: {rank}   FATIA: {fatia}')
#
#     print(f'\n[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] - INICIANDO O PROCESSAMENTO DAS EMPRESAS')
#
#     processos = c.proctempdao.listar_nao_processados(tag='EMPRESAS_REC', rank=rank, fatia=fatia, limit=1000)
#
#     while len(processos) > 0:
#
#         for id, processo in enumerate(processos, 1):
#             processo.processado = True
#             print(f'[ {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} ] - {id}/{len(processos)} - Verificando recuperandas no processo: {processo.numero}')
#             c.classifica_empresa_recuperanda_proc_temp(processo)
#             processo.encontrado = True
#             c.proctempdao.salvar(processo)
#
#         processos = c.proctempdao.listar_nao_processados(tag='EMPRESAS_REC', rank=rank, fatia=fatia, limit=1000)
#
#     print(f'\n[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] - PROCESSAMENTO DAS EMPRESAS FOI FINALIZADO')
#
#     # print(f'\n[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] - INICIANDO O PROCESSAMENTO DAS EMPRESAS\n')
#     #
#     # c.filtra_movimento_marcador(rank=rank, fatia=fatia, tag='FALENCIAS', dias=2000, random=False, distinct=True, limit=None)
#     #
#     # print(f'\n[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] - PROCESSAMENTO DAS EMPRESAS FOI FINALIZADO')
