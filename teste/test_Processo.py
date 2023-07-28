import unittest
from unittest import TestCase

from pdjus.modelo.Processo import Processo


class test_Processo(TestCase):

    # def test_processo_invalido_sem_numero_processo_com_grau(self):
    #     processo = Processo()
    #     processo.grau = 1
    #
    #     self.assertEqual(processo.is_valido(),False)

    def test_processo_valido_com_numero_processo_e_grau(self):
        processo = Processo()
        processo.grau = 1
        processo.numero_processo = "123454568"

        self.assertEqual(processo.is_valido(),True)

    # def test_processo_invalido_com_numero_processo_sem_grau(self):
    #     processo = Processo()
    #     processo.numero_processo = "123454568"
    #
    #     self.assertEqual(processo.is_valido(),False)
    #
    # def test_processo_invalido_sem_numero_processo_sem_grau(self):
    #     processo = Processo()
    #
    #     self.assertEqual(processo.is_valido(),False)
    #
    # def test_processo_invalido_sem_npu_com_grau(self):
    #     processo = Processo()
    #     processo.grau = 1
    #
    #     self.assertEqual(processo.is_valido(),False)

    def test_processo_valido_com_npu_e_grau(self):
        processo = Processo()
        processo.grau = 1
        processo.npu = "123454568"
        self.assertEqual(processo.is_valido(),True)

    # def test_processo_invalido_com_npu_sem_grau(self):
    #     processo = Processo()
    #     processo.npu = "123454568"
    #
    #     self.assertEqual(processo.is_valido(),False)
    #
    # def test_processo_invalido_sem_npu_sem_grau(self):
    #     processo = Processo()
    #
    #     self.assertEqual(processo.is_valido(),False)

if __name__ == '__main__':
    unittest.main()
