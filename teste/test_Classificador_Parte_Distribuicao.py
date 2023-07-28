from unittest import TestCase

from classificadores.ClassificaParteDistribuicao import ClassificaParteDistribuicao


class test_Classificador_Parte_Distribuicao(TestCase):


    def test_classificador_pj(self):
        classificaParteDistribuicao = ClassificaParteDistribuicao()
        with open('inputs/test_classificador_pj.dat') as texto:
            linhas_do_texto = texto.readlines()
            for idx,item in enumerate(linhas_do_texto):
                item = item.upper().strip("\n")
                if item != '\n':
                    pessoa_juridica, banco, pequena_empresa, governo, cobranca = classificaParteDistribuicao.classifica_parte_distribuicao(item)
                    if not pessoa_juridica:
                        print('ERRORS: PESSOA JURIDICA NAO ENCONTRADA')
                        print(item)

                    try:
                        self.assertTrue(pessoa_juridica)
                    except AssertionError as e:
                        if idx+1 < len(linhas_do_texto):
                            for linha in linhas_do_texto[idx+1:]:
                                linha = linha.upper().strip("\n")
                                if linha != '\n':
                                    pessoa_juridica, banco, pequena_empresa, governo, cobranca = classificaParteDistribuicao.classifica_parte_distribuicao(
                                        linha)
                                    if not pessoa_juridica:
                                        print(linha)
                            break

    def test_classificador_pf(self):
        classificaParteDistribuicao = ClassificaParteDistribuicao()
        with open('inputs/test_classificador_pf.dat') as texto:
            linhas_do_texto = texto.readlines()
            for idx,item in enumerate(linhas_do_texto):
                item = item.upper().strip("\n")
                if item != '\n':
                    pessoa_juridica, banco, pequena_empresa, governo, cobranca = classificaParteDistribuicao.classifica_parte_distribuicao(item)
                    if pessoa_juridica:
                        print('ERRORS: PESSOA FISICA ENCONTRADA')
                        print(item)
                        pessoa_juridica, banco, pequena_empresa, governo, cobranca = classificaParteDistribuicao.classifica_parte_distribuicao(
                            item)
                    try:
                        self.assertFalse(pessoa_juridica)
                    except AssertionError as e:
                        if idx+1 < len(linhas_do_texto):
                            for linha in linhas_do_texto[idx+1:]:
                                linha = linha.upper().strip("\n")
                                if linha != '\n':
                                    pessoa_juridica, banco, pequena_empresa, governo, cobranca = classificaParteDistribuicao.classifica_parte_distribuicao(
                                        linha)
                                    if pessoa_juridica:
                                        print(linha)
                            break