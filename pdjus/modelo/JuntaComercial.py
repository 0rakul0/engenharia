import re
from pdjus.modelo.BaseClass import *
from pdjus.modelo.Empresa import Empresa
from pdjus.modelo.TipoJunta import TipoJunta
from util.StringUtil import remove_acentos, remove_varios_espacos,remove_links,remove_caracteres_especiais

class JuntaComercial(BaseClass):
    id = PrimaryKeyField(null=False)
    numero_alteracao = CharField(db_column="numero_alteracao")
    _texto = CharField(db_column="texto")
    data = DateTimeField()
    data_caderno = DateTimeField()
    empresa = ForeignKeyField(Empresa, null=True)
    tipo_junta = ForeignKeyField(TipoJunta, null=True)
    _texto_corrigido = CharField(db_column="texto_corrigido")
    classificado = BooleanField(db_column="classificado")

    @property
    def texto(self):
        if self._texto:
            self._texto = remove_caracteres_especiais(remove_links(remove_varios_espacos(remove_acentos(self._texto.upper()))))

        return self._texto

    @texto.setter
    def texto(self, value):
        if value:
            self._texto = value

        else:
            self._texto = ''

    @property
    def texto_corrigido(self):
        self._texto_corrigido = remove_varios_espacos(remove_acentos(self._texto_corrigido.upper()))
        return self._texto_corrigido

    def is_valido(self):
        if not self.empresa:
            print("Não pode existir uma Junta Comercial sem uma empresa!")
            return False
        if not self.tipo_junta:
            print("Não pode existir uma Junta Comercial sem um tipo!")
            return False
        return True

    class Meta:
        db_table = "junta_comercial"