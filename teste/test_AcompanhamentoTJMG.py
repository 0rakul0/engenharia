# import unittest
#
# from acompanhamento_processual.AcompanhamentoProcessualMG import AcompanhamentoProcessualMG
# from teste.DbTestFactory import DbTestFactory
# from teste.test_AcompanhamentoBase import test_AcompanhamentoBase
#
#
# class test_AcompanhamentoTJMG(test_AcompanhamentoBase):
#
#     def setUp(self):
#         DbTestFactory()
#
#     def test_pega_processo_falencia(self):
#         self.generico_gera_arvore_processo(AcompanhamentoProcessualMG(),numero_processo="07565496020128130024",
#                                            classe_processual="MANDADO DE SEGURANCA",
#                                            advogados=['GERALDA DO CARMO SILVA','RONALDO DE PAULA'],
#                                            assunto=["ADMINISTRATIVO E OUTRAS MATÉRIAS DE PÚBLICO > SISTEMA NACIONAL DE TRÂNSITO > LIBERAÇÃO DE VEÍCULO APREENDIDO"],
#                                            comarca = "COMARCA DE BELO HORIZONTE",
#                                            partes=["MAURA DOS SANTOS CALDEIRA","DIRETOR DER MG DEPARTAMENTO DE ESTRADAS E RODAGEM ESTADO MG"])
#
#
# if __name__ == '__main__':
#     unittest.main()