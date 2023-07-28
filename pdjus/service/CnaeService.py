from pdjus.conexao.Conexao import Singleton
from pdjus.dal.CnaeDao import CnaeDao
from pdjus.modelo.Cnae import Cnae
from pdjus.modelo.CnaeObjetoSocial import CnaeObjetoSocial
from pdjus.dal.CnaeObjetoSocialDao import CnaeObjetoSocialDao
from classificadores.ClassificaCNAE import ClassificaCNAE
from pdjus.service.BaseService import BaseService
from util.StringUtil import remove_varios_espacos, remove_acentos,remove_caracteres_especiais
import re
class CnaeService(BaseService,metaclass=Singleton):

    def __init__(self):
        super(CnaeService, self).__init__(CnaeDao())

    def preenche_cnae(self, numero):
        cnae = None
        #numero = remove_caracteres_especiais(remove_varios_espacos(remove_acentos(numero.strip())))
        if numero != '':
            cnae = self.dao.get_por_numero(numero)
            if not cnae:
                cnae = Cnae()
                cnae.numero = numero
                self.salvar(cnae)

        return cnae
    def seta_cnae(self,objeto_social,cnae):
        cnae_objeto_social_dao = CnaeObjetoSocialDao()

        cnae = self.preenche_cnae(cnae)
        cnae_objeto_social = cnae_objeto_social_dao.get_por_cnae_objeto_social(cnae, objeto_social)
        if not cnae_objeto_social:
            cnae_objeto_social = CnaeObjetoSocial()
        cnae_objeto_social.cnae = cnae
        cnae_objeto_social.objeto_social = objeto_social
        #cnae_objeto_social.observacao = '7_digitos'
        cnae_objeto_social_dao.salvar(cnae_objeto_social)

    def verifica_objeto_social_cnae(self,objeto_social,lista_cnae=None):
        cnae_objeto_social_dao = CnaeObjetoSocialDao()
        classifica_cnae = ClassificaCNAE()

        nome_objeto = re.sub('\s+','',objeto_social._nome)

        if re.search('(EXISTEM\s*OUTRAS\s*ATIVIDADES|OBJETO\s*(SOCIAL)?\s*NAO\s*CADASTRADO)',objeto_social._nome):
            cnae = self.preenche_cnae('9999')
            cnae_objeto_social = cnae_objeto_social_dao.get_por_cnae_objeto_social(cnae, objeto_social)
            if not cnae_objeto_social:
                cnae_objeto_social = CnaeObjetoSocial()
                cnae_objeto_social.cnae = cnae
                cnae_objeto_social.objeto_social = objeto_social
                cnae_objeto_social_dao.salvar(cnae_objeto_social, commit=True, salvar_estrangeiras=False,salvar_many_to_many=False)
                print('Objeto ', objeto_social._nome, ' Atribuído ao CNAE: ', '9999')
            return True
        lista_cnae = classifica_cnae.preenche_lista_cnae(nome_objeto, lista_cnae_dic=lista_cnae)

        if len(lista_cnae)>0:
            for numero_cnae in lista_cnae:
                cnae = self.preenche_cnae(numero_cnae)
                cnae_objeto_social = cnae_objeto_social_dao.get_por_cnae_objeto_social(cnae, objeto_social)
                if not cnae_objeto_social:
                    cnae_objeto_social = CnaeObjetoSocial()
                    cnae_objeto_social.cnae = cnae
                    cnae_objeto_social.objeto_social = objeto_social
                    cnae_objeto_social_dao.salvar(cnae_objeto_social, commit=True,salvar_estrangeiras=False, salvar_many_to_many=False)
                    print('Objeto ',objeto_social._nome, ' Atribuído ao CNAE: ', numero_cnae)

                # if not objeto_social in cnae.objetos_sociais:
                #     cnae.objetos_sociais.append(objeto_social)
                #     self.dao.salvar(cnae,salvar_estrangeiras = False)
                #     print('Objeto ',objeto_social._nome, ' Atribuído ao CNAE: ', numero_cnae)
                #     return True
        else:
            print('Objeto ',objeto_social._nome,' Não foi atribuído a nenhum CNAE')
            return False

