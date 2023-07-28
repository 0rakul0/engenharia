# -*- coding: utf-8 -*-
from pdjus.modelo.BaseClass import *
from pdjus.modelo.Processo import Processo
from pdjus.modelo.Status import Status

class ProcessoStatus(BaseClass):
    id = PrimaryKeyField(null=False)
    processo_id = ForeignKeyField(Processo,null=True, db_column="processo_id")
    status_id = ForeignKeyField(Status, null=True,db_column="status_id")

    def is_valido(self):
        return True

    class Meta:
        db_table = "processo_status"
