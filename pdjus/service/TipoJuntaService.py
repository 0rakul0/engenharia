from pdjus.conexao.Conexao import Singleton
from pdjus.dal.TipoJuntaDao import TipoJuntaDao
from pdjus.service.BaseService import BaseService
from util.StringUtil import remove_acentos,remove_varios_espacos,remove_caracteres_especiais,remove_pontuacao
from pdjus.modelo.TipoJunta import TipoJunta

class TipoJuntaService(BaseService,metaclass=Singleton):


    def __init__(self):
        super(TipoJuntaService, self).__init__(TipoJuntaDao())

        self.tipo_junta_dict = {'ALTERACOESCOMANDITASSIMPLES': 'ALTERACOES COMANDITAS SIMPLES',
                                'ALTERACOESCONSORCIOS': 'ALTERACOES CONSORCIOS',
                                'ALTERACOESCOOPERATIVAS': 'ALTERACOES COOPERATIVAS',
                                'ALTERACOESEIRELI': 'ALTERACOES EIRELI',
                                'ALTERACOESEMPRESARIOS': 'ALTER AC OES EMPRESARIOS',
                                'ALTERACOESEMPRESASESTRANGEIRAS': 'ALTERACOES EMPRESAS ESTRANGEIRAS',
                                'ALTERACOESFIRMASINDIVIDUAIS': 'ALTERACOES FIRMAS INDIVIDUAIS',
                                'ALTERACOESFIRMASLIMITADAS': 'ALTERACOES FIRMAS LIMITADAS',
                                'ALTERACOESGENERICAS': 'ALTERACOES GENERICAS',
                                'ALTERACOESSOCIEDADESLIMITADAS': 'ALTERACOES SOCIEDADES LIMITADAS',
                                'ALTERACOESSOCIEDADESPORACOES': 'ALTERACOES SOCIEDADES POR ACOES',
                                'CONSTITUICOESCOMANDITASSIMPLES': 'CONSTITUICOES COMANDITAS SIMPLES',
                                'CONSTITUICOESCONSORCIOS': 'CONSTITUICOES CONSORCIOS',
                                'CONSTITUICOESCOOPERATIVAS': 'CONSTITUICOES COOPERATIVAS',
                                'CONSTITUICOESEIRELI': 'CONSTITUICOES EIRELI',
                                'CONSTITUICOESEMPRESARIOS': 'CONSTITUICOES EMPRESARIOS',
                                'CONSTITUICOESEMPRESASESTRANGEIRAS': 'CONSTITUICOES EMPRESAS ESTRANGEIRAS',
                                'CONSTITUICOESFIRMASINDIVIDUAIS': 'CONSTITUICOES FIRMAS INDIVIDUAIS',
                                'CONSTITUICOESFIRMASLIMITADAS': 'CONSTITUICOES FIRMAS LIMITADAS',
                                'CONSTITUICOESGENERICAS': 'CONSTITUICOES GENERICAS',
                                'CONSTITUICOESSOCIEDADESLIMITADAS': 'CONSTITUICOES SOCIEDADES LIMITADAS',
                                'CONSTITUICOESSOCIEDADESPORACOES': 'CONSTITUICOES SOCIEDADES POR ACOES'}

    def preenche_tipo_junta(self,nome):
        nome = remove_pontuacao(remove_caracteres_especiais(remove_varios_espacos(remove_acentos(nome.upper())))).replace(' ','')
        nome = self.tipo_junta_dict[nome]
        tipo = self.dao.get_por_nome(nome)
        if tipo is None:
            tipo = TipoJunta()
            tipo.nome = nome
            self.salvar(tipo)
        return tipo