from pdjus.dal.GenericoDao import GenericoDao, Singleton
from pdjus.modelo.Processo import Processo


class ObservacaoDao(GenericoDao,metaclass=Singleton):
    def __init__(self):
        super(ObservacaoDao, self).__init__(Processo)

    def get_por_observacao(self, processo, observacao):
        try:
            return self._classe.select().where(
                                               self._classe.processo == processo,
                                               self._classe.observacao == observacao,
                                               self._classe.grau == 2
                                               ).get()

        except self._classe.DoesNotExist as e:
            return None