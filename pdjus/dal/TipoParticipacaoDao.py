__author__ = 'B130019727'

from pdjus.dal.GenericoDao import GenericoDao,Singleton
from pdjus.modelo.TipoParticipacaoModel import TipoParticipacao
from util.StringUtil import remove_acentos,remove_varios_espacos


class TipoParticipacaoDao(GenericoDao,metaclass=Singleton):
    def __init__(self):
        super(TipoParticipacaoDao, self).__init__(TipoParticipacao)

    def get_por_nome(self, nome):
        try:
            if nome:
                nome = remove_varios_espacos(remove_acentos(nome.upper()))
                return self._classe.select().where(self._classe._nome == nome).get()
            else:
                return None
        except self._classe.DoesNotExist as e:
            return None