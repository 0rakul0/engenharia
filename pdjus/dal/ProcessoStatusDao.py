from pdjus.dal.GenericoDao import GenericoDao,Singleton
from pdjus.modelo.ProcessoStatus import ProcessoStatus

class StatusProcessoDao(GenericoDao, metaclass=Singleton):
    def __init__(self):
        super(StatusProcessoDao, self).__init__(ProcessoStatus)

    def get_por_status_e_processo(self, id_processo, status):
        try:
            if not status or not id_processo:
                return None
            else:
                return self._classe.select().where(
                    (self._classe.processo_id == id_processo) &
                    (self._classe.status_id == status)
                ).get()
        except self._classe.DoesNotExist:
            return None
