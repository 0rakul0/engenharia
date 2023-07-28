from unittest import TestCase

from datetime import datetime, timedelta

import numpy

import datedelta

from pdjus.conexao.Conexao import default_schema
from pdjus.service.DistribuicaoService import DistribuicaoService


class test_Indices(TestCase):
    pass
    #DEFASADO NÃO FAZ MAIS SENTIDO DO JEIOT QUE ESTÁ
    # def test_Contagem(self):
    #     if not "producao" in default_schema:
    #         print("ESTES TESTES SÓ FAZEM SENTIDO EM PRODUCAO, PARA VERIFICAR O VALOR GERADO DO INDICE DO MES")
    #         self.assertTrue(True)
    #         return
    #
    #     hoje = datetime.now()
    #     mes_passado = hoje - datedelta.datedelta(months=1)
    #     mes_retrasado = hoje - datedelta.datedelta(months=2)
    #     tres_meses_atras = hoje - datedelta.datedelta(months=3)
    #     quatro_meses_atras = hoje - datedelta.datedelta(months=4)
    #     distribuicao_service = DistribuicaoService()
    #     classes = ["TITULO *(EXECUTIVO)? *EXTR?A\-?JUDICIAL", "MONITORIA", "DESPEJ", "BUSC.*APREE?N.*ALIEN", "USUCAP",
    #               "ALUG|LOCAC!DESPEJ", "EXEC.*ALIMENTO", "ALIMENTO!EXEC"]
    #
    #     for classe in classes:
    #         qtd_distribuicoes_do_mes_passado = len(distribuicao_service.dao.listar_contagem_tag_por_mes("CLASSE_DISTRIBDIVERSOS", mes_passado.year, mes_passado.month, classe_processual=classe))
    #         qtd_distribuicoes_do_mes_retrasado = len(distribuicao_service.dao.listar_contagem_tag_por_mes("CLASSE_DISTRIBDIVERSOS", mes_retrasado.year, mes_retrasado.month, classe_processual=classe))
    #         qtd_distribuicoes_de_tres_meses_atras = len(distribuicao_service.dao.listar_contagem_tag_por_mes("CLASSE_DISTRIBDIVERSOS", tres_meses_atras.year, tres_meses_atras.month, classe_processual=classe))
    #         qtd_distribuicoes_de_quatro_meses_atras = len(distribuicao_service.dao.listar_contagem_tag_por_mes("CLASSE_DISTRIBDIVERSOS", quatro_meses_atras.year, quatro_meses_atras.month, classe_processual=classe))
    #
    #         lista_meses_anteriores = [qtd_distribuicoes_do_mes_retrasado,qtd_distribuicoes_de_tres_meses_atras,qtd_distribuicoes_de_quatro_meses_atras]
    #
    #         media = numpy.mean(lista_meses_anteriores)
    #         desvio_padrao = numpy.std(lista_meses_anteriores)
    #
    #         self.assertTrue(qtd_distribuicoes_do_mes_passado< media + (4*desvio_padrao),"Teve {} distribuicoes, muito mais distribuições do que o esperado na classe ".format(str(qtd_distribuicoes_do_mes_passado)) + classe + "no ano/mes " + str(mes_passado.year) +"/"+ str(mes_passado.month))
    #         self.assertTrue(qtd_distribuicoes_do_mes_passado > media - (4 * desvio_padrao),"Teve {} distribuicoes, muito menos distribuições do que o esperado na classe ".format(str(qtd_distribuicoes_do_mes_passado)) + classe + "no ano/mes " + str(mes_passado.year) +"/"+ str(mes_passado.month))
    #
    # def test_Contagem_Amostragem(self):
    #     if not "producao" in default_schema:
    #         print("ESTES TESTES SÓ FAZEM SENTIDO EM PRODUCAO, PARA VERIFICAR O VALOR GERADO DO INDICE DO MES")
    #         self.assertTrue(True)
    #         return
    #
    #     hoje = datetime.now()
    #     mes_passado = hoje - datedelta.datedelta(months=1)
    #     mes_retrasado = hoje - datedelta.datedelta(months=2)
    #     tres_meses_atras = hoje - datedelta.datedelta(months=3)
    #     quatro_meses_atras = hoje - datedelta.datedelta(months=4)
    #     distribuicao_service = DistribuicaoService()
    #     classes = ["TITULO *(EXECUTIVO)? *EXTR?A\-?JUDICIAL", "MONITORIA", "DESPEJ", "BUSC.*APREE?N.*ALIEN", "USUCAP",
    #               "ALUG|LOCAC!DESPEJ", "EXEC.*ALIMENTO", "ALIMENTO!EXEC"]
    #
    #     for classe in classes:
    #         qtd_distribuicoes_do_mes_passado = len(distribuicao_service.dao.listar_contagem_tag_por_mes("INDICE", mes_passado.year, mes_passado.month, classe_processual=classe))
    #         qtd_distribuicoes_do_mes_retrasado = len(distribuicao_service.dao.listar_contagem_tag_por_mes("INDICE", mes_retrasado.year, mes_retrasado.month, classe_processual=classe))
    #         qtd_distribuicoes_de_tres_meses_atras = len(distribuicao_service.dao.listar_contagem_tag_por_mes("INDICE", tres_meses_atras.year, tres_meses_atras.month, classe_processual=classe))
    #         qtd_distribuicoes_de_quatro_meses_atras = len(distribuicao_service.dao.listar_contagem_tag_por_mes("INDICE", quatro_meses_atras.year, quatro_meses_atras.month, classe_processual=classe))
    #
    #         lista_meses_anteriores = [qtd_distribuicoes_do_mes_retrasado,qtd_distribuicoes_de_tres_meses_atras,qtd_distribuicoes_de_quatro_meses_atras]
    #
    #         media = numpy.mean(lista_meses_anteriores)
    #         desvio_padrao = numpy.std(lista_meses_anteriores)
    #
    #         self.assertTrue(qtd_distribuicoes_do_mes_passado > 3000,"Teve {} distribuicoes, muito mais distribuições do que o esperado na classe ".format(str(qtd_distribuicoes_do_mes_passado)) + classe + " no ano/mes " + str(mes_passado.year) +"/"+ str(mes_passado.month))
