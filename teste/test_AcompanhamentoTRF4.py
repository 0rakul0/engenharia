import unittest

from acompanhamento_processual.AcompanhamentoProcessualDJSP import AcompanhamentoProcessualDJSP
from acompanhamento_processual.AcompanhamentoProcessualTRF4 import AcompanhamentoProcessualTRF4
from teste.DbTestFactory import DbTestFactory
from teste.test_AcompanhamentoBase import test_AcompanhamentoBase


class test_AcompanhamentoTRF4(test_AcompanhamentoBase):

    def setUp(self):
        DbTestFactory()

    def test_pega_processo(self):
        self.generico_gera_arvore_processo(AcompanhamentoProcessualTRF4(),numero_processo="200671000297921",
                                           classe_processual="PROCEDIMENTO DO JUIZADO ESPECIAL CÍVEL",
                                           orgao_julgador ='Juízo Federal da 18a VF de Porto Alegre',
                                           advogados='JONHSON HIPPEN',
                                           assunto='Benefício Assistencial (Art. 203,V CF/88)',comarca = 'Porto Alegre',juiz='Alberi Augusto Soares da Silva',
                                           partes=['LIOMAR DUARTE LEAO','INSTITUTO NACIONAL DO SEGURO SOCIAL - INSS'],movimentos=['Recebimento ORIG: SUPERINTENDÊNCIA DO INSS','Requisição de Pagamento - Pequeno Valor - Paga'],
                                           tag = 'TRF4')
if __name__ == '__main__':
    unittest.main()