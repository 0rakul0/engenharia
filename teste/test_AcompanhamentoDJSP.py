import unittest

from acompanhamento_processual.AcompanhamentoProcessualDJSP import AcompanhamentoProcessualDJSP
from teste.DbTestFactory import DbTestFactory
from teste.test_AcompanhamentoBase import test_AcompanhamentoBase


class test_AcompanhamentoDJSP(test_AcompanhamentoBase):

    def setUp(self):
        DbTestFactory()

    def test_pega_processo_falencia(self):
        self.generico_gera_arvore_processo(AcompanhamentoProcessualDJSP(),npu="00001705920008260070",numero_processo="070012000000170",
                                           classe_processual="FALENCIA DE EMPRESARIOS, SOCIEDADES EMPRESARIAIS, MICROEMPRESAS E EMPRESAS DE PEQUENO PORTE",
                                           assunto='RECUPERACAO JUDICIAL E FALENCIA',juiz='MARIA ESTHER CHAVES GOMES',tag="FALENCIAS",
                                           partes=['MERCANTIL FARMED LTDA','SILVIA APARECIDA NARDI ME','ESPOLIO DE JAIR ALBERTO CARMONA'],movimentos=['?Fica novamente intimado o exequente (síndico) para providenciar a atualização do débito e o recolhimento de taxa de pesquisa junto ao Bacenjud, no valor de R$ 10,00 (Cód. 434-1) para cada CPF, no prazo de 10 dias?.','Aguardando Prazo 15'])


if __name__ == '__main__':
    unittest.main()