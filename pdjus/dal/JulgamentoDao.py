from pdjus.dal.GenericoDao import GenericoDao, Singleton
from pdjus.modelo.Julgamento import Julgamento


class JulgamentoDao(GenericoDao,metaclass=Singleton):
    def __init__(self):
        super(JulgamentoDao, self).__init__(Julgamento)

    def get_por_tipo_participante_e_processo_e_juiz(self, tipo_participacao, processo, juiz):
        try:
            return self._classe.select().where(self._classe.processo == processo,
                                               self._classe.tipo_participacao == tipo_participacao,
                                               self._classe.juiz == juiz).get()

        except self._classe.DoesNotExist as e:
            return None


