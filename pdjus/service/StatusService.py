from pdjus.conexao.Conexao import Singleton
from pdjus.dal.StatusDao import StatusDao
from pdjus.modelo.Status import Status
from pdjus.service.BaseService import BaseService
from util.StringUtil import remove_tracos_pontos_barras_espacos, remove_acentos


class StatusService(BaseService,metaclass=Singleton):

    def __init__(self):
        super(StatusService, self).__init__(StatusDao())

    def preenche_status(self,nome_status):
        nome_status = remove_acentos(remove_tracos_pontos_barras_espacos(nome_status))
        status = self.dao.get_por_nome(nome_status.upper())

        if not status:
            status = Status()
            status.nome = nome_status.upper()
            self.salvar(status)
        return status