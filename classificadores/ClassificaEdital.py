# -*- coding: utf-8 -*-


import re
from pdjus.modelo.TipoParte import TipoParte
from pdjus.service.ProcessoService import ProcessoService
from pdjus.service.SituacaoProcessoService import SituacaoProcessoService
from util.FalenciaUtil import verifica_texto_decretacao_falencia

class ClassificaEdital:
    def __init__(self):
        self.processoService = ProcessoService()
        self.situacao_processo_service = SituacaoProcessoService()

    def valida(self,p,edital,data=None):
        processo = self.processoService.dao.get_por_numero_processo_ou_npu_e_tribunal(p.replace('.','').replace('-','').strip())
        if processo:
            # self.pega_cnpj(processo,edital)
            self.pega_decretacao_falencia(processo,edital,data)
            self.processoService.salvar(processo)

#Acredito que deva ser removido!
    def pega_cnpj(self,processo,edital):
        expressao_cnpj = re.compile("[Cc][Nn][Pp][Jj].*(\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2})",re.U)
        cnpj_match = expressao_cnpj.search(edital)
        if cnpj_match:
            cnpj = cnpj_match.group(1)
            print(cnpj)
            for parte_processo in processo.partes_processo:
                if parte_processo.tipo_parte_id == TipoParte.REU and parte_processo.parte.empresa:
                    parte_processo.parte.empresa.cnpj = cnpj


    def pega_decretacao_falencia(self,processo,edital,data):
        encontrou = verifica_texto_decretacao_falencia(edital)
        if encontrou:
            self.situacao_processo_service.preenche_situacao_processo(processo, 'DECRETADO', data)
            self.processoService.dao.salvar(processo)
