from pdjus.dal.GenericoDao import *
from pdjus.modelo.Setor import Setor

class SetorDao(GenericoDao,metaclass=Singleton):

    def __init__(self):
        super(SetorDao, self).__init__(Setor)

    def get_por_nome(self,nome):
        try:
            nome = remove_varios_espacos(remove_acentos(nome))
            obj = self._classe.get(self._classe._nome == nome)
            return obj
        except self._classe.DoesNotExist as e:
            return None
