import time
from classificadores.ClassificadorBaseML import ClassificadorBaseML


class ClassificaParteDistribuicaoML(ClassificadorBaseML):
    def __init__(self,arquivo_metodo="rais_sample3.LinearSVC",arquivo_origem=None,arquivo_destino=None,limite=9,parte_distribuicao_service=None):
        self.parte_distribuicao_service = parte_distribuicao_service
        super(ClassificaParteDistribuicaoML, self).__init__(arquivo_metodo,arquivo_origem, arquivo_destino,limite)
        
   
    def valida_setor_parte(self,parteDistribuicao):
        previsao = self._prever(parteDistribuicao.parte)
        if previsao:
            parteDistribuicao.setor = previsao

    

    def valida_setor_arquivo(self):
        i=0
        with open(self.arquivo_origem, "r", encoding="utf-8") as csv_file:
            print("Iniciando as previsoes")
            while True:
                linha = csv_file.readline()
                if not linha:
                    return
                value = linha.strip().split("\t")

                with open(self.arquivo_destino, "a", encoding="latin-1", newline="\n") as arquivo:
                    # print("id","razao_social", "setor_previsto", "score",file=arquivo,sep=";")

                    previsao = self._prever(value[3])
                    if previsao:
                        print(value[1].strip(),
                            value[3].strip(),  # razao social
                              previsao,  # valor previsto
                              str(self._get_higher_score(self.decision_function_matrix[0])).replace(".",
                                                                                         ",") if self.hasDecision else 0,
                              # score
                              file=arquivo, sep=";")

                        print(value[1].strip(),
                              value[3].strip(),  # razao social
                              previsao,  # valor previsto
                              str(self._get_higher_score(self.decision_function_matrix[0])).replace(".",",") if self.hasDecision else 0,# score
                              sep=";")
                i+=1
                print("Analisando linha: {}".format(str(i)))

    def incluir_setor(self):

        i=0

        start_time = time.time()
        tempo_atual = 0


        with open(self.arquivo_destino, "r", encoding="latin-1", newline="\n") as arquivo:
            for index in range(1,100000000000000):
                linha_csv = arquivo.readline()
                if not linha_csv:
                    self.parte_distribuicao_service.dao.commit()
                    return

                if index % 1000000 == 0 and index>0:
                    tempo_passado = tempo_atual
                    tempo_atual = (time.time() - start_time)
                    print("Exectuado em {} milhões de linhas".format(str(index / 1000000)))
                    print("--- tempo total:  %s segundos ---" % (time.time() - start_time))
                    print("--- tempo atual:  %s segundos ---" % str(abs(tempo_passado - tempo_atual)))


                estrutura_csv = linha_csv.split(";")

                id = estrutura_csv[0]
                setor = estrutura_csv[2]
                parte_distribuicao = self.parte_distribuicao_service.dao.get_por_id(id)
                if parte_distribuicao.pessoa_juridica:
                    print(estrutura_csv[0],";",estrutura_csv[1],";",estrutura_csv[2])
                    parte_distribuicao.setor = setor
                    self.parte_distribuicao_service.salvar(parte_distribuicao,commit=False)
                    i+=1

                    if i % 5000 == 0:
                        self.parte_distribuicao_service.dao.commit()






   
#
# if __name__ == "__main__":
#     if len(sys.argv) > 1:
#         ClassificaParteDistribuicaoML("rais_sample3.LinearSVC", "parte_distribuicao.csv", "resultados//resultado_parte_distribuicao-{}.csv".format(sys.argv[1])).incluir_setor()
#     else:
#         ClassificaParteDistribuicaoML("rais_sample3.LinearSVC", "parte_distribuicao.csv", "resultado_parte_distribuicao.csv").incluir_setor()