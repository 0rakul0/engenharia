from pdjus.conexao.Conexao import Singleton
from pdjus.dal.ObservacaoDao import ObservacaoDao
from pdjus.modelo.Processo import Processo
from pdjus.service.BaseService import BaseService

class ObservacaoService(BaseService, metaclass=Singleton):

    def __init__(self):
        super(ObservacaoService, self).__init__(ObservacaoDao())

    def preenche_observacao(self, observacao):
        processo = Processo()
        if processo.observacao is not None:
          observacao = self.dao.get_por_observacao(processo, observacao)

        if not observacao:
          observacao = Processo()
          observacao.observacao = observacao
          observacao.grau = 2
          self.salvar(observacao)
        return observacao