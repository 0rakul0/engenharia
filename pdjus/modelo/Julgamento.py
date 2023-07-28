from pdjus.modelo.BaseClass import *
from util.StringUtil import remove_acentos, remove_varios_espacos
from pdjus.modelo.Processo import Processo
from pdjus.modelo.Juiz import Juiz
from pdjus.modelo.TipoParticipacaoModel import TipoParticipacao


class Julgamento(BaseClass):
    id = PrimaryKeyField(null=False)
    # tipo_participante = CharField(db_column='tipo_participante', null=False)
    tipo_participacao = ForeignKeyField(TipoParticipacao, null=False)
    processo = ForeignKeyField(Processo, null=False)
    juiz = ForeignKeyField(Juiz, null=False)

    def __init__(self, *args, **kwargs):
        self.init_on_load(*args, **kwargs)

    def init_on_load(self, *args, **kwargs):
        super(Julgamento, self).__init__("nome", *args, **kwargs)

    def is_valido(self):
        if not self.juiz or not self.processo or not self.tipo_participacao:
            print("Não pode existir um julgamento sem os campos de juiz,processo e tipo de participacao!")
            return False
        return True

# nome da tabela
    class Meta:
        db_table = "julgamento"