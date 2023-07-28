from pdjus.conexao.Conexao import Singleton
from pdjus.dal.JulgamentoDao import JulgamentoDao
from pdjus.modelo.Julgamento import Julgamento
from pdjus.service.BaseService import BaseService

class JulgamentoService(BaseService, metaclass=Singleton):

    def __init__(self):
        super(JulgamentoService, self).__init__(JulgamentoDao())

    def preenche_julgamento(self, tipo_participacao, processo, juiz):
        if processo.id and juiz.id and tipo_participacao.id is not None:
            julgamento = self.dao.get_por_tipo_participante_e_processo_e_juiz(tipo_participacao, processo, juiz)

        if julgamento is None:
                julgamento = Julgamento()
                julgamento.tipo_participacao = tipo_participacao
                julgamento.juiz = juiz
                julgamento.processo = processo
                self.salvar(julgamento)
        return julgamento
