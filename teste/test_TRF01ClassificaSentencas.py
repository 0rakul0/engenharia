# import unittest
# from unittest import TestCase
# import shutil, os, os.path
# from classificadores.ClassificaTRF01Sentencas import ClassificaTRF01Sentencas
#
# class test_TRF01ClassificaSentencas(TestCase):
#
#     def setUp(self):
#         self.apaga_se_existir ('sentencas.dat')
#         self.apaga_se_existir ('sentencas-classificadas.dat')
#         self.apaga_se_existir ('sentencas-nao-classificadas.dat')
#
#     def tearDown(self):
#         self.apaga_se_existir ('sentencas.dat')
#         self.apaga_se_existir ('sentencas-classificadas.dat')
#         self.apaga_se_existir ('sentencas-nao-classificadas.dat')
#
#     def apaga_se_existir(self, arquivo):
#         if os.path.isfile(arquivo):
#             os.remove(arquivo)
#
#     def generico_classificacao_sentecas(self, classe):
#
#         shutil.copy('inputs/sentencas_'+classe+'.dat', 'sentencas.dat')
#
#         classificador = ClassificaTRF01Sentencas()
#         classificador.run()
#
#         for chunk in classificador.le_arquivo_para_dataframe('sentencas-classificadas.dat'):
#
#             for index, c in classificador.itera_chunk(chunk):
#
#                 if c[classe] != 1:
#                     print(c['tipo_movimento'])
#                     print(c['texto_movimento'])
#
#                 self.assertEqual(c[classe], 1)
#
#
#     def test_classifica_sentenca_sem_merito(self):
#         self.generico_classificacao_sentecas('sem_merito')
#
#
#     def test_classifica_sentenca_emb_acolhidos_parc(self):
#         self.generico_classificacao_sentecas('emb_parc_acolhidos')
#
#
#     def test_classifica_sentenca_parcial_proc(self):
#         self.generico_classificacao_sentecas('parcial_proc')
#
#
#     def test_classifica_sentenca_improc(self):
#         self.generico_classificacao_sentecas('improc')
#
#
#     def test_classifica_sentenca_procedente(self):
#         self.generico_classificacao_sentecas('procedente')
#
#
#     def test_classifica_sentenca_emb_acolhidos(self):
#         self.generico_classificacao_sentecas('emb_acolhidos')
#
#
#     def test_classifica_sentenca_emb_rejeit(self):
#         self.generico_classificacao_sentecas('emb_rejeit')
#
#
#     def test_classifica_sentenca_acordo(self):
#         self.generico_classificacao_sentecas('acordo')
#
#     def test_generico_classificador_falso_positivo(self):
#         classes = ['sem_merito', 'parcial_proc', 'improc', 'procedente', 'emb_acolhidos', 'emb_parc_acolhidos',
#                    'emb_rejeit', 'acordo']
#
#         for classe in classes:
#             for idxb in classes:
#                 if classe != idxb:
#                     shutil.copy ('inputs/sentencas_' + classe + '.dat', 'sentencas.dat')
#                     print (classe, idxb)
#                     classificador = ClassificaTRF01Sentencas()
#                     classificador.run ()
#
#                     for chunk in classificador.le_arquivo_para_dataframe ('sentencas-classificadas.dat'):
#                         for index, c in classificador.itera_chunk (chunk):
#                             if c[idxb] != 0:
#                                 print (c['tipo_movimento'])
#                                 print (c['texto_movimento'])
#
#                             self.assertNotEqual (c[idxb], 1)
#
#
# if __name__ == '__main__':
#     unittest.main()