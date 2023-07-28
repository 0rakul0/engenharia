import unittest
from unittest import TestCase
import shutil, os, os.path
from classificadores.ClassificaQuadroCredores import ClassificaQuadroCredores

class test_QuadrodeCredor(TestCase):


    def test_valida_sim_quadro(self):
        validaQuadro = ClassificaQuadroCredores(tag="FALENCIAS")
        texto = open('inputs/SIM_QUADRO')
        linhas_do_texto = texto.readlines()
        texto.close()
        for idx,item in enumerate(linhas_do_texto):
            if item != '\n':
                item = item.upper()
                resultado = validaQuadro.verifica_possibilidade_de_quadro(item)
                if not resultado:
                    print('ERRORS: VALIDA SIM QUADRO')
                    print(item)

                try:
                    self.assertTrue(resultado)
                except AssertionError as e:
                    if idx+1 < len(linhas_do_texto):
                        for linha in linhas_do_texto[idx+1:]:
                            if linha != '\n':
                                resultado = validaQuadro.verifica_possibilidade_de_quadro(linha)
                                if not resultado:
                                    print(linha)
                        # break
                    raise e


    def test_valida_nao_quadro(self):
        validaQuadro = ClassificaQuadroCredores(tag="FALENCIAS")
        texto = open('inputs/NAO_QUADRO')
        linhas_do_texto = texto.readlines()
        texto.close()
        for idx,item in enumerate(linhas_do_texto):
            if item != '\n':
                item = item.upper()
                resultado = validaQuadro.verifica_possibilidade_de_quadro(item)
                if resultado is True:
                    print('ERRORS: VALIDA NÃO QUADRO')
                    print(item)

                try:
                    self.assertFalse(resultado)
                except AssertionError as e:
                    if idx+1 < len(linhas_do_texto):
                        for linha in linhas_do_texto[idx+1:]:
                            if linha != '\n':
                                resultado = validaQuadro.verifica_possibilidade_de_quadro(linha)
                                if resultado:
                                    print(linha)
                        # break
                    raise e

                self.assertFalse(resultado)
if __name__ == '__main__':
    unittest.main()