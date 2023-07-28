from pdjus.modelo.BaseClass import *
from pdjus.modelo.Cnae import Cnae
from pdjus.modelo.Setor import Setor

class CnaeSetor (BaseClass):
    id = PrimaryKeyField(null=False)
    cnae = ForeignKeyField(Cnae, null=True)
    setor = ForeignKeyField(Setor, null=True)

    def is_valido(self):
        if not self.cnae:
            print("Não pode existir um Cnae Setor sem Cnae!")
            return False
        if not self.setor:
            print("Não pode existir um Cnae Setor sem Setor!")
            return False
        return True

    class Meta:
        db_table = "cnae_setor"