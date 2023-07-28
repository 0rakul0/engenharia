__author__ = 'B130019727'

from pdjus.conexao.Conexao import Singleton
from pdjus.dal.TipoParticipacaoDao import TipoParticipacaoDao
from pdjus.modelo.TipoParticipacaoModel import TipoParticipacao
from pdjus.service.BaseService import BaseService


class TipoParticipacaoService(BaseService,metaclass=Singleton):

    def __init__(self):
        super(TipoParticipacaoService, self).__init__(TipoParticipacaoDao())

    def preenche_tipo_participacao(self, nome):
        tipoParticipacao = self.dao.get_por_nome(nome)
        if not tipoParticipacao:
            tipoParticipacao = TipoParticipacao()
            tipoParticipacao.nome = nome
            self.salvar(tipoParticipacao)
        return tipoParticipacao