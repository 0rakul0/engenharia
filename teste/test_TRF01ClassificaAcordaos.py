# import unittest
# from unittest import TestCase
# import shutil, os, os.path
# from classificadores.ClassificaTRF01Acordaos import ClassificaTRF01Acordaos
#
#
# class test_ClassificaTRF01Acordaos(TestCase):
#
#     def setUp(self):
#         self.apaga_se_existir ('recursos.dat')
#         self.apaga_se_existir ('recursos-classificadas.dat')
#         self.apaga_se_existir ('recursos-nao-classificadas.dat')
#
#     def tearDown(self):
#         self.apaga_se_existir ('recursos.dat')
#         self.apaga_se_existir ('recursos-classificadas.dat')
#         self.apaga_se_existir ('recursos-nao-classificadas.dat')
#
#     def apaga_se_existir(self, arquivo):
#         if os.path.isfile(arquivo):
#             os.remove(arquivo)
#
#     def generico_classificacao_recursos(self, classe):
#
#         shutil.copy('inputs/recursos_'+classe+'.dat', 'recursos.dat')
#
#         classificador = ClassificaTRF01Acordaos()
#         classificador.run()
#
#         for chunk in classificador.le_arquivo_para_dataframe('recursos-classificadas.dat'):
#
#             for index, c in classificador.itera_chunk(chunk):
#
#                 if c[classe] != 1:
#                     print(c['tipo_movimento'])
#                     print(c['texto_movimento'])
#
#                 self.assertEqual(c[classe], 1)
#
#     def test_classifica_sentenca_provido_parcial(self):
#         self.generico_classificacao_recursos('provido_parcial')
#
#
#     def test_classifica_sentenca_provido(self):
#         self.generico_classificacao_recursos('provido')
#
#
#     def test_classifica_sentenca_negado(self):
#         self.generico_classificacao_recursos('negado')
#
#
#     def test_generico_classificador_falso_positivo(self):
#         classes = ['provido_parcial','provido','negado']
#
#         for classe in classes:
#             for idxb in classes:
#                 if classe != idxb:
#                     shutil.copy ('inputs/recursos_' + classe + '.dat', 'recursos.dat')
#                     print (classe, idxb)
#                     classificador = ClassificaTRF01Acordaos()
#                     classificador.run ()
#
#                     for chunk in classificador.le_arquivo_para_dataframe ('recursos-classificadas.dat'):
#                         for index, c in classificador.itera_chunk (chunk):
#                             if c[idxb] != 0:
#                                 print (c['tipo_movimento'])
#                                 print (c['texto_movimento'])
#
#                             self.assertNotEqual (c[idxb],1)
#
#
# if __name__ == '__main__':
#     unittest.main()