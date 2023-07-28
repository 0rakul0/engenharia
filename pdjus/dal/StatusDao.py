from pdjus.dal.GenericoDao import GenericoDao,Singleton
from pdjus.modelo.Status import Status
from pdjus.modelo.ProcessoStatus import ProcessoStatus
from util.StringUtil import remove_varios_espacos, remove_acentos


class StatusDao(GenericoDao,metaclass=Singleton):
    def __init__(self):
        super(StatusDao, self).__init__(Status)

    def get_por_nome(self, nome):
        try:
            nome = remove_varios_espacos(remove_acentos(nome.upper()))
            return self._classe.get(self._classe._nome == nome)

        except self._classe.DoesNotExist as e:
            return None