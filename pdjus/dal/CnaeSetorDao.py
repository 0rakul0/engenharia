from pdjus.conexao.Conexao import Singleton
from pdjus.dal.GenericoDao import GenericoDao
from pdjus.modelo.CnaeSetor import CnaeSetor

class CnaeSetorDao(GenericoDao,metaclass=Singleton):
    def __init__(self):
        super(CnaeSetorDao, self).__init__(CnaeSetor)

    def get_por_cnae_setor(self, cnae, setor):
        try:
            return self._classe.select().where(self._classe.cnae==cnae,self._classe.setor==setor).get()
        except self._classe.DoesNotExist as e:
            return None