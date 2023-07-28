# -*- coding: utf-8 -*-

import unittest
import regex
from extrator.ExtratorTRF import ExtratorTRF
import os

class test_ExtratorTRF(unittest.TestCase):
    pass

    #OS TESTES ESTAO REFERENCIANDO UMA PASTA NÃO RELATIVA PRECISA ATUALIZAR

    # def test_TRF01_JUD_SJAM_2017_02_08(self):
    #     # testa regexes no arquivo descrito na assinatura do método
    #     arquivo = "TRF01_JUD_SJAM_2017_02_08.txt"
    #     arquivo = os.path.join('Z:\\TRF\\TRF01\\txt\\2017\\02', arquivo)
    #
    #     with open(arquivo, encoding='utf-8', mode='r', errors="ignore") as arq:
    #         e = ExtratorTRF(arq, None)
    #         regex01 = e.regex_publicacao
    #         contents = e.limpa_cabecalhos()
    #
    #         match_num = len(regex.findall(regex01, contents, flags=e.flags))
    #
    #     self.assertGreaterEqual(match_num, 39)
    #
    # def test_TRF01_JUD_SJDF_2015_08_25(self):
    #     arquivo = "TRF01_JUD_SJDF_2015_08_25.txt"
    #     arquivo = os.path.join('Z:\\TRF\\TRF01\\txt\\2015\\08', arquivo)
    #
    #     with open(arquivo, encoding='utf-8', mode='r', errors="ignore") as arq:
    #         e = ExtratorTRF(arq, None)
    #
    #         regex01 = e.regex_publicacao
    #
    #         contents = e.limpa_cabecalhos()
    #
    #         num = len(regex.findall(regex01, contents, flags=e.flags))
    #
    #     self.assertGreaterEqual(num, 280)
    #
    #
    # # 4288-82.2007.4.01.3200
    # def test_TRF01_JUD_SJAM_2017_02_08_2(self):
    #     # testa regexes no arquivo descrito na assinatura do método
    #     arquivo = "TRF01_JUD_SJAM_2017_02_08.txt"
    #     arquivo = os.path.join('Z:\\TRF\\TRF01\\txt\\2017\\02', arquivo)
    #
    #     with open(arquivo, encoding='utf-8', mode='r', errors="ignore") as arq:
    #
    #         e = ExtratorTRF(arq, None)
    #         regex01 = e.regex_publicacao
    #         contents = e.limpa_cabecalhos()
    #
    #         (num, tipo, partes, texto, ultimo) = regex.findall(regex01, contents, flags=e.flags)[0]
    #
    #     self.assertEqual(num.strip(), "11933-22.2011.4.01.3200")
    #
    # def test_TRF01_JUD_SJRO_2015_07_27(self):
    #     arquivo = "TRF01_JUD_SJRO_2015_07_27.txt"
    #     arquivo = os.path.join('Z:\\TRF\\TRF01\\txt\\2015\\07', arquivo)
    #
    #     with open(arquivo, encoding='utf-8', mode='r', errors="ignore") as arq:
    #
    #         e = ExtratorTRF(arq, None)
    #
    #         regex01 = e.regex_publicacao
    #
    #         contents = e.limpa_cabecalhos()
    #
    #         num = len(regex.findall(regex01, contents, flags=e.flags))
    #
    #     self.assertGreaterEqual(num, 180)


if __name__ == '__main__':
    unittest.main()