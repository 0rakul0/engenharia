from classificadores.ClassificaQuadroCredores import ClassificaQuadroCredores
from classificadores.ClassificadorBaseML import ClassificadorBaseML
from pdjus.service.BlocoQuadroService import BlocoQuadroService
from pdjus.service.QuadroCredorService import QuadroCredorService


class ClassificaQuadroCredorML(ClassificadorBaseML):
    def __init__(self, arquivo_metodo="quadro_classificado.BernoulliNB", arquivo_origem=None, arquivo_destino=None, limite=0):
        super(ClassificaQuadroCredorML, self).__init__(arquivo_metodo, arquivo_origem, arquivo_destino, limite)
        
    def classifica_quadro(self,texto):
        previsao = self._prever(texto)
        if previsao == "True":
            return True
        return False


if __name__ == "__main__":
    bloco_service = BlocoQuadroService()
    classificador = ClassificaQuadroCredorML()
    classifica_quadro = ClassificaQuadroCredores(tag="FALENCIAS")

    blocos = bloco_service.dao.listar(limit=3000)
    unicos_blocos = list(set([bloco.texto for bloco in blocos]))
    print(len(unicos_blocos))
    with open("quadros_regex_ml.csv", "w") as file:
        for texto in unicos_blocos:
            texto = texto
            classe = classificador.classifica_quadro(texto)
            classe_regex = classifica_quadro.verifica_possibilidade_de_quadro(texto)
            texto = texto.replace(";",",")
            if not classe == classe_regex:
                file.write(texto+'"'+";'"+str(classe_regex)+"'\n")
            if classe == classe_regex and classe == True:
                print(texto+'"'+";'"+str(classe_regex)+"'\n")