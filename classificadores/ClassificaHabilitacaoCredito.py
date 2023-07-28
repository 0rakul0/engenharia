# -*- coding: utf-8 -*-
from decimal import *
import re
from pdjus.modelo.Processo import Processo
from pdjus.service.MovimentoService import MovimentoService
from pdjus.service.SentencaService import SentencaService
from util.RegexUtil import RegexUtil
from pdjus.modelo.Sentenca import Sentenca
from pdjus.dal.SentencaDao import SentencaDao
from util.StringUtil import acerta_valor_string_para_decimal
class ClassificaHabilitacaoCredito:

    def __init__(self, tag):
        self.tag = tag

    def verifica_habilitacao_credito(self,movimento):
        if self.__is_tipo_movimento_sentenca_hab_credito(movimento.tipo_movimento):
            match, classe_credito, tipo_moeda, valor = self.verifica_habilitacao_deferida(movimento.texto)
            if match:
                # print('\nHABILITAÇÃO DEFERIDA! Classe de crédito {}, Valor Habilitado {}{}'.format(classe_credito,tipo_moeda,valor))
                # print(movimento.texto)
                try:
                    sentencaService = SentencaService()
                    sentencaService.preenche_sentenca(movimento=movimento,situacao='HABILITACAO DEFERIDA',data=movimento.data,tipo_moeda=tipo_moeda,valor=acerta_valor_string_para_decimal(valor),descricao=classe_credito)
                except Exception as e:
                    print('Movimento: {} Valor: {}'.format(movimento.id,valor))
                    # print(movimento.texto)
                    # print(movimento.processo.npu_ou_num_processo)
            else:
                match = self.verifica_habilitacao_indeferida(movimento.texto)
                if match:
                    # print('\nHABILITAÇÃO INDEFERIDA!, {} PROC nº {}'.format(movimento.id,movimento.processo.npu_ou_num_processo))
                    # print(movimento.texto)
                    sentencaService = SentencaService()
                    sentencaService.preenche_sentenca(processo=movimento.processo,movimento=movimento, situacao='HABILITACAO INDEFERIDA',data=movimento.data)
        # else:
        #     print('\nNÃO É SENTENÇA DE HABILITAÇÃO DE CRÉDITO: {}'.format(movimento.texto))


    def verifica_habilitacao_deferida(self,texto): #FICAR ATENTO: QUALQUER MODIFICACAO NOS REGEX TEM QUE ALTERAR O VALOR DOS GRUPOS
        classe_credito = None
        tipo_moeda = None
        valor = None
        match = re.search(RegexUtil.regex_habilitacao_deferidos_padrao1, texto, re.IGNORECASE)
        if match:
            classe_credito = match.group(24)
            tipo_moeda = match.group(7)
            valor = match.group(8)
        else:
            match = re.search(RegexUtil.regex_habilitacao_deferidos_padrao2, texto, re.IGNORECASE)
            if match:
                classe_credito = match.group(5)
                tipo_moeda = match.group(30)
                valor = match.group(31)
            else:
                match = re.search(RegexUtil.regex_habilitacao_deferidos_padrao3, texto, re.IGNORECASE)
                if match:
                    classe_credito = match.group(10)
                    tipo_moeda = match.group(35)
                    valor = match.group(35)
        return match, classe_credito,tipo_moeda,valor

    def __is_tipo_movimento_sentenca_hab_credito(self, tipo_movimento):
        return ('DECISAO' in tipo_movimento.nome.upper() or 'DESPACHO' in tipo_movimento.nome.upper() or \
               'SENTENCA' in tipo_movimento.nome.upper() or 'JULG' in tipo_movimento.nome.upper() or\
                'PROFERID' in tipo_movimento.nome.upper() or\
                re.search(RegexUtil.regex_habilitacao_indeferidos_tp_mov, tipo_movimento.nome, re.IGNORECASE)) and\
                    'TRANSITO EM JULGADO' not in tipo_movimento.nome.upper()

    def verifica_habilitacao_indeferida(self, texto):
        match = (re.search(RegexUtil.regex_habilitacao_indeferidos_padrao1, texto, re.IGNORECASE) or \
                re.search(RegexUtil.regex_habilitacao_indeferidos_padrao2, texto, re.IGNORECASE) or \
                re.search(RegexUtil.regex_habilitacao_indeferidos_padrao3, texto, re.IGNORECASE) or \
                re.search(RegexUtil.regex_habilitacao_indeferidos_padrao4, texto, re.IGNORECASE) or \
                re.search(RegexUtil.regex_habilitacao_indeferidos_padrao5, texto, re.IGNORECASE))
        return match

if __name__ == '__main__':
    movimento_service = MovimentoService()
    classificaHabCred = ClassificaHabilitacaoCredito('FALENCIAS')
    print("DEFERIDAS")
    for i in range (0,10):
        movimentos = movimento_service.dao.listar_possiveis_sentencas_habilitacao_credito_deferidas(rank=i,fatia=10)
        for movimento in list(set(movimentos)):
            classificaHabCred.verifica_habilitacao_credito(movimento)
