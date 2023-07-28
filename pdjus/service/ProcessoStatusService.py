from datetime import datetime

from pdjus.conexao.Conexao import Singleton
from pdjus.dal.ProcessoStatusDao import StatusProcessoDao
from pdjus.modelo.Status import Status
from pdjus.modelo.Processo import Processo
from pdjus.service.BaseService import BaseService
from pdjus.dal.StatusDao import StatusDao
from pdjus.modelo.ProcessoStatus import ProcessoStatus
from pdjus.service.StatusService import StatusService


class ProcessoStatusService(BaseService,metaclass=Singleton):

    def __init__(self):
        super(ProcessoStatusService, self).__init__(StatusProcessoDao())

    def preenche_staus_processo(self, id_processo, status):

        statusService = StatusService()
        status = statusService.preenche_status(status)

        processo_status = None

        if id_processo:
            processo_status = self.dao.get_por_status_e_processo(id_processo,status)

        if not processo_status:
            processo_status = ProcessoStatus()
            processo_status.status_id = status
            processo_status.processo_id = id_processo
            self.salvar(processo_status)

        return processo_status
