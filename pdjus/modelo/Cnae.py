from pdjus.modelo.BaseClass import *
from util.StringUtil import remove_acentos, remove_varios_espacos,remove_links
from pdjus.modelo.Setor import Setor

class Cnae(BaseClass):
    id = PrimaryKeyField(null=False)
    _numero = CharField(db_column="numero")


    def __init__(self,*args, **kwargs):
      self.init_on_load(*args, **kwargs)

    def init_on_load(self,*args, **kwargs):
        super(Cnae, self).__init__("numero",*args, **kwargs)

    def is_valido(self):
        if not self._numero:
            print("Não pode existir um cnae sem nome!")
            return False
        return True

    @property
    def numero(self):
        self._numero = remove_links(remove_varios_espacos(remove_acentos(self._numero.upper())))
        return self._numero

    @numero.setter
    def numero(self, value):
        self._numero = remove_links(remove_varios_espacos(remove_acentos(value.upper())))
