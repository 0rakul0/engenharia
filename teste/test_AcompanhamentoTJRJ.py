import unittest

from acompanhamento_processual.AcompanhamentoProcessualRJ import AcompanhamentoProcessualRJ
from teste.DbTestFactory import DbTestFactory
from teste.test_AcompanhamentoBase import test_AcompanhamentoBase


class test_AcompanhamentoTJRJ(test_AcompanhamentoBase):

    def setUp(self):
        DbTestFactory()

    def test_pega_processo_falencia(self):
        self.generico_gera_arvore_processo(AcompanhamentoProcessualRJ(),npu="0000227-29.1998.8.19.0010",
                                           classe_processual="HABILITACAO DE CREDITO",
                                           assunto='CLASSIFICACAO DE CREDITOS',
                                           partes=['GREENSTAR TELECOMUNICACAO LTDA','FERREIRA E BORGES & CIA. LTDA.','JOAO BATISTA FERREIRA BORGES'],movimentos=['DESCRICAO: CERTIFICO E DOU FE QUE, ATE A PRESENTE DATA, NAO HOUVE MANIFESTACAO SOBRE O ATO ORDINATORIO DE FL. 132.'])


if __name__ == '__main__':
    unittest.main()