import re

class criarLista():
    def __init__(self):
        self.lista_npu=[]

    def gerar_lista(self, caminho):
        with open(caminho) as arq:
            for line in arq:
                line = line.replace('\n','')
                self.lista_npu.append(line)
            arq.close()
        return self.lista_npu

if __name__ == "__main__":
    func = criarLista()
    processos = func.gerar_lista(r'C:\Users\b13001972777\Documents\a_extrair.txt')
    processos_unicos = list(set(processos))
    print(f'processos = {processos_unicos}')
    print(len(processos_unicos))
