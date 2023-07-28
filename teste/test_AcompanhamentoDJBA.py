import unittest
from acompanhamento_processual.AcompanhamentoProcessualDJBA import AcompanhamentoProcessualDJBA
from teste.DbTestFactory import DbTestFactory
from teste.test_AcompanhamentoBase import test_AcompanhamentoBase

class test_AcompanhamentoDJBA(test_AcompanhamentoBase):

    def setUp(self):
        DbTestFactory()

    def test_pega_processo_falencia(self):
        self.generico_gera_arvore_processo(AcompanhamentoProcessualDJBA(),npu="00014048920098050088",advogados="NAYDSON LEAO FIGUEIREDO,DIMAS MEIRA MALHEIROS", assunto="Recuperação judicial e Falência",
                                           classe_processual="FALÊNCIA DE EMPRESÁRIOS, SOCIEDADES EMPRESÁRIAIS, MICROEMPRESAS E EMPRESAS DE PEQUENO PORTE",
                                           partes=['Nordeste Tratores Ltda','Bahia Solo Comercial de Produtos Agropecuarios Ltda.','Florisvaldo Pereira da Silva','Guanambi Comercio de Tratores e Implementos Agriculas Ltda'],
                                           movimentos=['TIPO BAIXA: ARQUIVAMENTO COM BAIXA OBSERVAÇÃO: PROCESSO JULGADO EM 30.11.2010. USUÁRIO: SFERNANDES','DATA PUBLICADO: 10/02/11 USUÁRIO: DPJ',
                                                       'DATA A SER PUBLICADO: 10/02/2011 USUÁRIO: SFERNANDES','JUIZ: JOÃO BATISTA PEREIRA PINTO OBSERVAÇÃO: JULGADO EXTINTO POR FALTA DE INTERESSE DA(S) PARTE(S). USUÁRIO: JLAZEVEDO',
                                                       'TIPO DE DOCUMENTO: CERTIDÃO OBSERVAÇÃO: AGUARDANDO MANIFESTAÇÃO (AÇÃO) USUÁRIO: VANASCIMENTO','DATA PUBLICADO: 15/04/10 USUÁRIO: DPJ',
                                                       'DATA A SER PUBLICADO: 15/04/2010 USUÁRIO: SFERNANDES',
                                                       'DATA A SER PUBLICADO: 15/04/2010 USUÁRIO: SFERNANDES',
                                                       'JUIZ: JOÃO BATISTA PEREIRA PINTO OBSERVAÇÃO: DETERMINADA A ABERTURA DE VISTA À PARTE AUTORA PARA MANIFESTAR INTERESSE, INDICANDO DILIGÊNCIA EM 05 (CINCO) DIAS. AGUARDANDO PUBLICAÇÃO. USUÁRIO: JLAZEVEDO'
                                                       ,'TIPO DE CONCLUSÃO: PARA DESPACHO/DECISÃO OBSERVAÇÃO: CLS. EM 25.03.09. USUÁRIO: SFERNANDES'
                                                       ,'ORIGEM: BEL. NAYDSON LEÃO FIGUEIREDO OBSERVAÇÃO: DEVOLVIDO SEM MANIFESTAÇÃO EM 02.02.09. USUÁRIO: SFERNANDES',
                                                       'TIPO DE CONCLUSÃO: PARA DESPACHO/DECISÃO OBSERVAÇÃO: AUTOS RECEBIDOS DA VARA CRIME DESTA COMARCA. CONCLUSOS EM 02/03/2009. USUÁRIO: EARANHA'
                                                       ,'USUÁRIO: EARANHA'
                                                       ,'TIPO: COMPETÊNCIA EXCLUSIVA VARA: 1A V DOS FEITOS DE REL DE CONS CIV E COMERCIAIS USUÁRIO: EARANHA'])


if __name__ == '__main__':
    unittest.main()