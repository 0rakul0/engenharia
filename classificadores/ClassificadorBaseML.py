import pickle

import numpy as np


class ClassificadorBaseML:
    def __init__(self,arquivo_metodo,arquivo_origem=None,arquivo_destino=None,limite=9):
        self.diretorio = "classificadores//arquivos_ml//"
        self.limite = limite
        self._carrega_caminhos_arquivos(arquivo_origem, arquivo_destino, arquivo_metodo)

        self._carrega_metodo(self.arquivo_vetor, self.arquivo_metodo)

    def _carrega_caminhos_arquivos(self, arquivo_origem, arquivo_destino, arquivo_metodo):
        if arquivo_origem and self.diretorio[:-2] in arquivo_origem:
            self.arquivo_origem = arquivo_origem
        elif arquivo_origem:
            self.arquivo_origem = self.diretorio + arquivo_origem
        if arquivo_destino and self.diretorio[:-2] in arquivo_destino:
            self.arquivo_destino = arquivo_destino
        elif arquivo_destino:
            self.arquivo_destino = self.diretorio + arquivo_destino
        if self.diretorio[:-2] in arquivo_metodo:
            self.arquivo_metodo = arquivo_metodo
            self.arquivo_vetor = arquivo_metodo.split(".")[0] + ".vetor"
        else:
            self.arquivo_metodo = self.diretorio + arquivo_metodo
            self.arquivo_vetor = self.diretorio + arquivo_metodo.split(".")[0] + ".vetor"

    def _carrega_metodo(self, arquivo_vetor, arquivo_metodo):
        with open(arquivo_vetor, "rb") as file:
            self.vetor = pickle.load(file)
        with open(arquivo_metodo, "rb") as file:
            self.metodo = pickle.load(file)
            
    def _prever(self, nome):
        X_set = self.vetor.transform([nome.replace(".", " ").replace("-", " ").strip()])

        previsoes = self.metodo.predict(X_set)
        if hasattr(self.metodo, 'decision_function'):
            self.hasDecision = True
            self.decision_function_matrix = self.metodo.decision_function(X_set)
        else:
            self.hasDecision = False

        if self.hasDecision:
            previsao = previsoes[0]
            scr = self.decision_function_matrix[0] if self.hasDecision else 0
            if self._get_higher_score(scr) > ((self.limite - 1) * 0.25):
                return previsao

        return None

    def _get_higher_score(self, values):
        max = float('-inf')
        for v in np.nditer(values):
            if v > max:
                max = v

        return max
