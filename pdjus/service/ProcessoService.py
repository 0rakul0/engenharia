from datetime import datetime

from pdjus.conexao.Conexao import Singleton
from pdjus.dal.ProcessoDao import ProcessoDao
from pdjus.modelo.Processo import Processo
from pdjus.service.AreaService import AreaService
from pdjus.service.AssuntoService import AssuntoService
from pdjus.service.BaseService import BaseService
from pdjus.service.ClasseProcessualService import ClasseProcessualService
from pdjus.service.JuizService import JuizService
from pdjus.service.ReparticaoSegundoGrauService import ReparticaoSegundoGrauService
from pdjus.service.ReparticaoService import ReparticaoService
from util.StringUtil import remove_tracos_pontos_barras_espacos, remove_caracteres_especiais, remove_acentos, \
    remove_varios_espacos


class ProcessoService(BaseService, metaclass=Singleton):

    def __init__(self):
        super(ProcessoService, self).__init__(ProcessoDao())

    def seta_numero_themis(self, processo, numero_themis):
        numero_themis = remove_tracos_pontos_barras_espacos(numero_themis)
        if not processo:
            processo = Processo()
        processo.numero_themis = numero_themis

    def seta_numero_processo(self, processo, numero_processo):
        numero_processo = remove_tracos_pontos_barras_espacos(numero_processo)
        if not processo:
            processo = Processo()
        processo.numero_processo = numero_processo

    def seta_data_distribuicao(self, processo, data_distribuicao, tipo_distibuicao=None):
        if not processo.data_distribuicao and data_distribuicao:
            processo.data_distribuicao = datetime.strptime(data_distribuicao, "%d/%m/%Y").date()
        if tipo_distibuicao:
            processo.tipo_distribuicao = remove_varios_espacos(
                remove_caracteres_especiais(remove_acentos(tipo_distibuicao)))

    def seta_valor_acao(self, valor, tipo_moeda, processo):
        # if not processo.valor_da_acao:
        processo.valor_da_acao = valor
        processo.tipo_moeda = tipo_moeda

    def seta_relator(self, processo, relator):
        if not processo.relator and relator:
            processo.relator = remove_caracteres_especiais(remove_acentos(remove_varios_espacos(relator.upper())))

    def preenche_processo_senha(self, npu=None, numero_processo=None, grau=None, senha=None, tribunal=None,
                        tag=None,  referencia=None, caderno=None, db_codigo=None, observacao=None):
        com_senha = None
        if npu:
            com_senha = self.dao.get_por_npu_senha_codigo(npu=npu, grau=grau, senha=senha, db_codigo=db_codigo )

        if not com_senha:
            com_senha = Processo()
            if npu:
                self.seta_npu(com_senha, npu)
            if numero_processo:
                self.seta_numero_processo(com_senha, numero_processo)
            if grau:
                com_senha.grau = grau
            if senha:
                com_senha.senha = senha
            if referencia and observacao == None:
                com_senha.processo_primeiro_grau_id = referencia
            if referencia and observacao:
                com_senha.processo_principal = referencia
            if db_codigo:
                com_senha.codigo = db_codigo
            if observacao:
                com_senha.observacao = observacao
            self.salvar(com_senha, caderno=caderno, tag=tag)
        return com_senha

    def preenche_processo_senha_primeiro(self, npu=None, numero_processo=None, grau=None, senha=None, tribunal=None,
                        tag=None,  caderno=None, db_codigo=None, observacao=None):
        processo_primeiro = None
        if npu:
            processo_primeiro = self.dao.get_por_npu_grau_codigo(npu=npu, grau=grau, db_codigo=db_codigo)

        if not processo_primeiro:
            processo_primeiro = Processo()
            if npu:
                self.seta_npu(processo_primeiro, npu)
            if numero_processo:
                self.seta_numero_processo(processo_primeiro, numero_processo)
            if grau:
                processo_primeiro.grau = grau
            if senha:
                processo_primeiro.senha = senha
            if db_codigo:
                processo_primeiro.codigo = db_codigo
            if observacao:
                processo_primeiro.observacao = observacao
            self.salvar(processo_primeiro, caderno=caderno, tag=tag)
        else:
            if npu:
                self.seta_npu(processo_primeiro, npu)
            if numero_processo:
                self.seta_numero_processo(processo_primeiro, numero_processo)
            if grau:
                processo_primeiro.grau = grau
            if senha:
                processo_primeiro.senha = senha
            self.salvar(processo_primeiro, caderno=caderno, tag=tag)

        return processo_primeiro

    def preenche_processo_codigo(self, npu=None, numero_processo=None, grau=None, caderno=None, tribunal=None, tag=None,
                          is_processos_com_mesmo_npu=False, db_codigo=None):
        processo = None
        if npu:
            processo = self.dao.get_por_npu_grau_codigo(npu, grau=grau, db_codigo=db_codigo)
        if not processo and numero_processo:
            processo = self.dao.get_por_numero_processo_ou_npu_e_tribunal(numero_processo, grau, tribunal,
                                                                          is_processos_com_mesmo_npu=is_processos_com_mesmo_npu)
        if not processo:
            processo = Processo()
            if npu:
                self.seta_npu(processo, npu)
            if numero_processo:
                self.seta_numero_processo(processo, numero_processo)
            if grau:
                processo.grau = grau
                self.salvar(processo, tag=tag)
            if db_codigo:
                processo.codigo = db_codigo
                self.salvar(processo, caderno=caderno, tag=tag)
        return processo

    def preenche_processo(self, npu=None, numero_processo=None, grau=None, tribunal=None, tag=None,
                          is_processos_com_mesmo_npu=False):
        processo = None
        if npu:
            processo = self.dao.get_por_numero_processo_ou_npu_e_tribunal(npu, grau, tribunal,
                                                                          is_processos_com_mesmo_npu=is_processos_com_mesmo_npu)
        if not processo and numero_processo:
            processo = self.dao.get_por_numero_processo_ou_npu_e_tribunal(numero_processo, grau, tribunal,
                                                                          is_processos_com_mesmo_npu=is_processos_com_mesmo_npu)
        if not processo:
            processo = Processo()
            if npu:
                self.seta_npu(processo, npu)
            if numero_processo:
                self.seta_numero_processo(processo, numero_processo)
            if grau:
                processo.grau = grau
                self.salvar(processo, tag=tag)
        return processo

    def preenche_sem_processo(self, npu=None, numero_processo=None, data=None, tag=None, grau=None, caderno=None, tribunal=None, is_processos_com_mesmo_npu=False, db_codigo=None, observacao=None):
        processo = None
        if npu:
            processo = self.dao.get_por_npu_grau_codigo(npu=npu, grau=grau, db_codigo=db_codigo)
        if not processo and numero_processo:
            processo = self.dao.get_por_numero_processo_ou_npu_e_tribunal(numero_processo, grau, tribunal,
                                                                          is_processos_com_mesmo_npu=is_processos_com_mesmo_npu)
        if not processo:
            processo = Processo()
            if npu:
                self.seta_npu(processo, npu)
            if numero_processo:
                self.seta_numero_processo(processo, numero_processo)
            if data:
                processo.data_atualizacao_recurso = data
            if grau:
                processo.grau = grau
            if db_codigo:
                processo.codigo = db_codigo
            if observacao:
                processo.observacao = observacao

            self.salvar(processo, caderno=caderno, tag=tag)

        return processo

    def preenche_sem_processo_primeiro(self, npu=None, numero_processo=None, data=None, tag=None, grau=None, caderno=None,
                              tribunal=None, is_processos_com_mesmo_npu=False, db_codigo=None, observacao=None):
        processo = None
        if npu:
            processo = self.dao.get_por_npu_grau_codigo(npu=npu, grau=grau, db_codigo=db_codigo)
        if not processo and numero_processo:
            processo = self.dao.get_por_numero_processo_ou_npu_e_tribunal(numero_processo, grau, tribunal,
                                                                          is_processos_com_mesmo_npu=is_processos_com_mesmo_npu)
        if not processo:
            processo = Processo()
            if npu:
                self.seta_npu(processo, npu)
            if numero_processo:
                self.seta_numero_processo(processo, numero_processo)
            if data:
                processo.data_atualizacao_recurso = data
            if grau:
                processo.grau = grau
            if db_codigo:
                processo.codigo = db_codigo
            if observacao:
                processo.observacao = observacao

            self.salvar(processo, caderno=caderno, tag=tag)
        else:
            if npu:
                self.seta_npu(processo, npu)
            if numero_processo:
                self.seta_numero_processo(processo, numero_processo)
            if data:
                processo.data_atualizacao_recurso = data
            if grau:
                processo.grau = grau
            if db_codigo:
                processo.codigo = db_codigo
            if observacao:
                processo.observacao = observacao

            self.salvar(processo, caderno=caderno, tag=tag)

        return processo

    def seta_npu(self, processo, npu):
        npu = remove_tracos_pontos_barras_espacos(npu)
        if not processo:
            processo = Processo()
        processo.npu = npu

    def seta_codigo(self, processo, db_codigo):
        db_codigo = remove_tracos_pontos_barras_espacos(db_codigo)
        if not processo:
            processo = Processo()
        processo.codigo = db_codigo

    def seta_reparticao(self, processo, nome_reparticao, comarca=None, tribunal=None):
        if nome_reparticao:
            reparticaoService = ReparticaoService()
            processo.reparticao = reparticaoService.preenche_reparticao(nome_reparticao, comarca, tribunal)

    def seta_reparticao_segundo_grau(self, processo, nome_reparticao, tribunal=None):
        if nome_reparticao:
            reparticaoServiceSegundoGrau = ReparticaoSegundoGrauService()
            processo.reparticao = reparticaoServiceSegundoGrau.preenche_reparticao_segundo_grau(nome_reparticao,
                                                                                                tribunal)

    def seta_juiz(self, processo, nome_juiz):
        if nome_juiz:
            juizService = JuizService()
            processo.juiz = juizService.preenche_juiz(nome_juiz)

    def seta_classe_processual(self, processo, classe, codigo_classe=None):
        if classe:
            classe_processualService = ClasseProcessualService()

            if not processo.classe_processual or processo.classe_processual.nome != classe:
                classe_processual = classe_processualService.preenche_classe_processual(classe)

                processo.classe_processual = classe_processual

    def seta_assunto(self, processo, nome_assunto, cod_assunto=None):
        assuntoService = AssuntoService()

        if processo:
            assunto = assuntoService.preenche_assunto(nome_assunto, cod_assunto)
            if not assunto in processo.assuntos:
                processo.assuntos.append(assunto)

    def seta_lista_assuntos(self, processo, lista_assuntos):
        for item_assunto in lista_assuntos:
            if item_assunto:
                self.seta_assunto(processo, item_assunto)

    def seta_processo_principal(self, processo, num_processo_principal, grau, tribunal=None, db_codigo=None):
        if tribunal:
            processo_principal = self.dao.get_por_numero_processo_ou_npu_e_tribunal(num_processo_principal, grau,
                                                                                    tribunal)
        else:
            processo_principal = self.dao.get_por_npu_grau_codigo(num_processo_principal, grau, db_codigo=db_codigo)

        if processo_principal:
            processo.processo_principal = processo_principal

        return processo_principal

    def referencia_primeiro_grau(self, processo, npu_primeiro_grau, grau=1, tag=None, tribunal=None, db_codigo=None):
        if tribunal:
            processo_primeiro = self.dao.get_por_numero_processo_ou_npu_e_tribunal(npu_primeiro_grau, tribunal)
        else:
            processo_primeiro = self.dao.get_por_npu_grau_codigo(npu_primeiro_grau, grau, db_codigo=db_codigo)
        if processo_primeiro:
            processo.processo_primeiro_grau_id = processo_primeiro
        return processo_primeiro

    def seta_processo_principal_sem_buscar_no_banco(self, processo_principal, processo_filho):
        if not processo_filho.processo_principal:
            processo_filho.processo_principal = processo_principal
        elif processo_principal.npu_ou_num_processo != processo_filho.processo_principal.npu_ou_num_processo:
            print(
                'PROBLEMA COM PROCESSO PRINCIPAL E VINCULADO, JÁ EXISTE UM PRINCIPAL CADASTRADO E NÃO É ESTE PROCESSO!')

    def seta_area(self, processo, nome_area):
        if not processo.area or processo.area.nome != nome_area:
            areaService = AreaService()
            area = areaService.preenche_area(nome_area)
            processo.area = area

    def seta_orgao_julgador(self, processo,  orgao_julgador):
        if not processo.orgao_julgador or orgao_julgador:
            orgao_julgador_texto = remove_caracteres_especiais(remove_acentos(remove_varios_espacos(orgao_julgador.upper())))
            processo.orgao_julgador = orgao_julgador_texto

    def seta_observacao(self, processo, observacao):
        if not processo.observacao or observacao:
            observacao_texto = remove_varios_espacos(remove_acentos(observacao.upper()))
            processo.observacao = observacao_texto

    def seta_secao(self, processo, secao):
        if not processo.secao or secao:
            secao_texto = remove_caracteres_especiais(remove_acentos(remove_varios_espacos(secao.upper())))
            processo.secao = secao_texto

    def seta_primeiro_grau(self, processo, primeiro_grau):
        if not processo.processo_primeiro_grau_id or primeiro_grau:
            processo.processo_primeiro_grau_id = primeiro_grau

    def seta_apenso_vinculado(self, processo, apenso):
        if not processo.apneso_vinculado_segundo_grau_id or apenso:
            apenso.apneso_vinculado_segundo_grau_id = processo