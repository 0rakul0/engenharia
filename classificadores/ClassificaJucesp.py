import re
from util.StringUtil import remove_varios_espacos, remove_acentos,remove_caracteres_especiais
from pdjus.service.TipoAnotacaoService import TipoAnotacaoService
from pdjus.dal.TipoAnotacaoJuntaComercialDao import TipoAnotacaoJuntaComercialDao
from pdjus.modelo.TipoAnotacaoJuntaComercial import TipoAnotacaoJuntaComercial
from util.RegexUtil import RegexUtil
class ClassificaJucesp:


    def classica_anotacao(self,junta_comercial,regex_util=None,constitucao=False):
        deu_match = False

        if constitucao:
            self.salva_constituicao(junta_comercial)
            deu_match = True
        else:
            for regex in regex_util.regex_tipo_anotacoes:
                if regex[0].search(junta_comercial.texto):
                    if regex[1] == 'indisponibilidade_de_cotas':
                        if re.search('LEVANTAMENTO\s*DO\s*BLOQUEIO|SEJA\s*(CANCELADA|LEVANTADA)\s*A\s*PENHORA|(DESBLOQ.{1,20}|LIBERACAO\s*DAS\s*)(QU|C)OTAS|DELEGACIA\s*DA\s*RECEITA',junta_comercial.texto):
                            continue
                    deu_match = True
                    self.salvar_relacao(regex,junta_comercial)
            if not deu_match:
                for regex in regex_util.regex_tipo_anotacoes_residual:
                    if regex[0].search(junta_comercial.texto):
                        deu_match = True
                        self.salvar_relacao(regex, junta_comercial)
        # if not deu_match:
        #     deu_match = True
        #     self.salvar_relacao('NAO_CLASSIFICADA', junta_comercial)
        return deu_match
            # if re.search("CONSTITUICOES", junta_comercial.tipo_junta.nome):
            #     tipo_anotacao = tipo_anotacao_service.preenche_tipo_anotacao('constituicao')
            #     # tipo_anotacao_junta_comercial = tipo_anotacao_junta_comercial_dao.get_por_tipo_anotacao_junta_comercial(junta_comercial, tipo_anotacao)
            #     # if not tipo_anotacao_junta_comercial:
            #     tipo_anotacao_junta_comercial = TipoAnotacaoJuntaComercial()
            #     tipo_anotacao_junta_comercial.junta_comercial = junta_comercial
            #     tipo_anotacao_junta_comercial.tipo_anotacao = tipo_anotacao
            #
            #     # tipo_anotacao_junta_comercial.observacao = observacao
            #     tipo_anotacao_junta_comercial_dao.salvar(tipo_anotacao_junta_comercial)
            #     print(junta_comercial.texto, 'classificado como constituicao')
            #     break

    def salvar_relacao(self,regex,junta_comercial):
        tipo_anotacao_service = TipoAnotacaoService()
        tipo_anotacao_junta_comercial_dao = TipoAnotacaoJuntaComercialDao()
        tipo_anotacao = tipo_anotacao_service.preenche_tipo_anotacao(regex[1])
        if tipo_anotacao:
            tipo_anotacao_junta_comercial = tipo_anotacao_junta_comercial_dao.get_por_tipo_anotacao_junta_comercial(junta_comercial, tipo_anotacao)
            if not tipo_anotacao_junta_comercial:
                tipo_anotacao_junta_comercial = TipoAnotacaoJuntaComercial()
                tipo_anotacao_junta_comercial.junta_comercial = junta_comercial
                tipo_anotacao_junta_comercial.tipo_anotacao = tipo_anotacao

                # tipo_anotacao_junta_comercial.observacao = observacao
                tipo_anotacao_junta_comercial_dao.salvar(tipo_anotacao_junta_comercial, commit=True,salvar_estrangeiras=False, salvar_many_to_many=False)
                print(junta_comercial.texto, 'classificado como', regex[1])

    def salva_constituicao(self,junta_comercial):
        tipo_anotacao_service = TipoAnotacaoService()
        tipo_anotacao_junta_comercial_dao = TipoAnotacaoJuntaComercialDao()
        tipo_anotacao = tipo_anotacao_service.preenche_tipo_anotacao('CONSTITUICAO')
        if tipo_anotacao:
            tipo_anotacao_junta_comercial = tipo_anotacao_junta_comercial_dao.get_por_tipo_anotacao_junta_comercial(
                junta_comercial, tipo_anotacao)
            if not tipo_anotacao_junta_comercial:
                tipo_anotacao_junta_comercial = TipoAnotacaoJuntaComercial()
                tipo_anotacao_junta_comercial.junta_comercial = junta_comercial
                tipo_anotacao_junta_comercial.tipo_anotacao = tipo_anotacao
                # tipo_anotacao_junta_comercial.observacao = observacao
                tipo_anotacao_junta_comercial_dao.salvar(tipo_anotacao_junta_comercial, commit=True,
                                                         salvar_estrangeiras=False, salvar_many_to_many=False)
                print(junta_comercial.texto, 'classificado como constituicao')
    def insere_tipo_banco(self):
        regex_util = RegexUtil()
        tipo_anotacao_service = TipoAnotacaoService()
        for regex in regex_util.regex_tipo_anotacoes:
            tipo_anotacao_service.preenche_tipo_anotacao(regex[1])



if __name__ == '__main__':
    c = ClassificaJucesp()
    c.insere_tipo_banco()