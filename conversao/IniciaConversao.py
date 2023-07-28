# -*- coding: utf-8 -*-
import sys
import traceback
from conversao.Conversor2 import Conversor
from util.ConfigManager import ConfigManager
import multiprocessing


def _converte_diario(diarios):
    for diario in diarios:
        try:
            conversor = Conversor(diario[0], diario[1])
            conversor.converte_diretorio()
        except Exception as e:  # capture todas as exceções
            print(f"Erro ao converter diário: {diario}. Erro: {str(e)}")
            traceback.print_exc()

class IniciaConversao(object):
    def __pedacos(self, l, n):
        newn = int(1.0 * len(l) / n + 0.5)
        for i in range(0, n-1):
            yield l[i*newn:i*newn+newn]
        yield l[n*newn-newn:]

    def inicia_conversao(self):
        log = "log_conversao.txt"
        diretorio = "RAIZ"
        erro = "erro_conversao.txt"
        extracoes = [
            ("DJRR", "pdf"),
        ]

        try:
            num_procs = multiprocessing.cpu_count()
            ConfigManager().escreve_log("Iniciando conversão {} processos.".format(num_procs), diretorio, log)
        except NotImplementedError:
            num_procs = 4
            ConfigManager().escreve_log("Não foi possível detectar a quantidade de núcleos. "
                                        "Iniciando conversão com {} processos (padrão).".format(num_procs),
                                        diretorio, log)

        pool = multiprocessing.Pool(num_procs)

        jobs = list(self.__pedacos(extracoes, num_procs))

        pool.map(_converte_diario, jobs)

        pool.close()

        ConfigManager().escreve_log("Conversão concluída. Verificar os logs individuais para possíveis erros.",
                                    diretorio, log)


if __name__ == '__main__':
    ie = IniciaConversao()
    ie.inicia_conversao()
