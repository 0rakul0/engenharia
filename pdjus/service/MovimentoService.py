from datetime import datetime

from pdjus.conexao.Conexao import Singleton
from pdjus.dal.MovimentoDao import MovimentoDao
from pdjus.modelo.Movimento import Movimento
from pdjus.modelo.TipoMovimento import TipoMovimento
from pdjus.modelo.Marcador import Marcador
from pdjus.modelo.MovimentoMarcador import MovimentoMarcador
from pdjus.service.BaseService import BaseService
from pdjus.service.TipoMovimentoService import TipoMovimentoService
from pdjus.service.MarcadorService import MarcadorService
from pdjus.dal.MovimentoMarcadorDao import MovimentoMarcadorDao


class MovimentoService(BaseService,metaclass=Singleton):

    def __init__(self):
        super(MovimentoService, self).__init__(MovimentoDao())

    def preenche_movimento_lote(self, processo, lista_movimentos):
        for movimento in lista_movimentos:
            self.preenche_movimento(processo, data=movimento['DATA'], texto=movimento['TEXTO'], tipoMovimento=movimento['TIPO'], julgamento=movimento['JULGAMENTO'])

    def seta_movimento_marcador(self, movimento, nome_marcador):
        marcadorService = MarcadorService()
        movimentoMarcadorDao = MovimentoMarcadorDao()

        if movimento:
            marcador = marcadorService.preenche_marcador(nome_marcador)
            movimento_marcador = movimentoMarcadorDao.get_por_movimento_marcador(movimento, marcador)

            if not movimento_marcador:
                movimento_marcador = MovimentoMarcador()
                movimento_marcador.movimento = movimento
                movimento_marcador.marcador = marcador
                movimentoMarcadorDao.salvar(movimento_marcador)

    def preenche_movimento_julgamento(self,processo,data=datetime.now(),texto=None,tipoMovimento=None,julgamento=None, observacao=None):

        if tipoMovimento and not type(tipoMovimento) is TipoMovimento:
            tipoMovimentoService = TipoMovimentoService()
            tipoMovimento = tipoMovimentoService.preenche_tipo_movimento(tipoMovimento)

        movimento = self.dao.get_por_processo_data_tipo_movimento_texto_julgamento(processo,data,tipoMovimento,texto,julgamento,hash_search=True)
        alterou = False
        if movimento is None:
            movimento = Movimento()
            movimento.data = data
            movimento.tipo_movimento = tipoMovimento
            movimento.julgamento_movimento = julgamento
            movimento.texto = texto
            movimento.processo = processo
            alterou = True
        if movimento and movimento.julgamento_movimento != julgamento:
            movimento.julgamento_movimento = julgamento
            alterou = True
        if movimento and observacao:
            movimento.observacao = observacao
            alterou = True
        if alterou:
            self.salvar(movimento, salvar_estrangeiras=False, commit=False)

        if not movimento:
            movimento = Movimento()
            movimento.tipo_movimento = tipoMovimento
            movimento.texto = texto
            movimento.julgamento_movimento = julgamento
            movimento.data = data
            movimento.processo = processo
            movimento.observacao = observacao
            self.salvar(movimento,salvar_estrangeiras=False,commit=False)

        return movimento

    def preenche_movimento(self,processo,data=datetime.now(),texto=None,tipoMovimento=None,nota_expediente=None, observacao=None):

        if tipoMovimento and not type(tipoMovimento) is TipoMovimento:
            tipoMovimentoService = TipoMovimentoService()
            tipoMovimento = tipoMovimentoService.preenche_tipo_movimento(tipoMovimento)

        movimento = self.dao.get_por_processo_data_tipo_movimento_texto(processo, data, tipoMovimento, texto, hash_search=True)
        alterou = False
        if movimento is None:
            movimento = Movimento()
            movimento.data = data
            movimento.tipo_movimento = tipoMovimento
            movimento.texto = texto
            movimento.processo = processo
            alterou = True
        if movimento and observacao:
            movimento.observacao = observacao
            alterou = True
        if movimento and nota_expediente:
            movimento.observacao = observacao
            alterou = True
        if alterou:
            self.salvar(movimento, salvar_estrangeiras=False, commit=False)

        if not movimento:
            movimento = Movimento()
            movimento.tipo_movimento = tipoMovimento
            movimento.texto = texto
            movimento.nota_expediente = nota_expediente
            movimento.data = data
            movimento.processo = processo
            movimento.observacao = observacao
            self.salvar(movimento,salvar_estrangeiras=False,commit=False)

        return movimento

    def atualiza_movimento(self, movimento, texto):

        alterou = False
        if movimento:
            movimento.texto = texto
            alterou = True
        if alterou:
            self.salvar(movimento, salvar_estrangeiras=False, commit=False)

        return movimento