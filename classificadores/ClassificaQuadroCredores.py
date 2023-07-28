 # -*- coding: utf-8 -*-
from decimal import *
import re

from pdjus.service.MovimentoService import MovimentoService
from pdjus.service.ProcessoService import ProcessoService
from pdjus.service.QuadroCredorService import QuadroCredorService
from pdjus.service.ClasseCredorService import ClasseCredorService
from pdjus.service.BlocoQuadroService import BlocoQuadroService
from util.StringUtil import remove_acentos, remove_varios_espacos
from util.ConfigManager import ConfigManager
from multiprocessing import Process, Manager
from util.RegexUtil import RegexUtil
import sys

class ClassificaQuadroCredores:
    # regex_quadro_artigo = '((ART(\.|IGO))\s(52|7|96|102)\D|(QUADRO|RELACAO|EDITAL(\sDE\sCONVOCACAO)?)\s(GERAL)?\s?DE\sCREDOR(ES)?).*?(CLASSE|QUIROGRA\w*|TRABALH\w*|TRIBUT\w*|GARANTIA\sREAL|CR[ÉE]DITO)'
    # regex_quadro_simples = 'EDITAL.*?(\sD[OE]S?\sCREDORES).*?\$'
    # regex_moedas = 'BRL|USD|R\$|US\$|U\$|EUR|£|GBP|€|¥|JPY|CLP|CHF|NOK|SEK'
    # regex_quadro_excluir_encerramento = '(ENCERRAMENTO|DECRETA[ÇC][AÃ]O)\s+D[AE]\s+FAL[ÊE]NCIA'
    # regex_quadro_indicacao_relacao = 'RELA[ÇC][ÃA]O\sD[OEA]S?\sCREDOR(ES)?\sAPRESENTAD'

    def __init__(self,tag):
        self.tag = tag
        # self.regex_quadro_artigo =       '((ART(\.|IGO))\s(52|7|96|102)\D|(EDITAL\s)?\\b(QGC|ROL|LISTA|QUADRO|RELACAO|EDITAL(\sDE\sCONVOCACAO)?)\s(GERAL)?\s?.{0,50}D(OS|E)\sCREDOR(ES)?|FORAM RECONHECIDOS PEL[AO] (ADM(|\.|INISTRADORA?) JUDICIAL|SINDICO) OS SEGUINTES CREDITOS|QGC|RELACAO CONSOLIDADA).{0,600}(CLASSE|QUIROGRA\w*|TRABALHIST\w*|TRIBUT\w*|GARANTIA\sREAL|\$)'
        # # self.regex_quadro_sem_classe = '((ART(\.|IGO))\s(52|7|96|102)\D|(EDITAL\s)?(ROL|LISTA|QUADRO|RELACAO|EDITAL(\sDE\sCONVOCACAO)?)\s(GERAL)?\s?.{0,50}D(OS|E)\sCREDOR(ES)?).{0,500}\$'
        # self.regex_moedas = 'BRL|USD|R\$|US\$|U\$|EUR|£|GBP|€|¥|JPY|CLP|CHF|NOK|SEK'
        # self.regex_quadro_excluir_encerramento = '(ENCERRAMENTO|DECRETA[ÇC][AÃ]O)\s+D[AE]\s+FAL[ÊE]NCIA'
        # self.regex_quadro_indicacao_relacao = 'RELA[ÇC][ÃA]O\sD[OEA]S?\sCREDOR(ES)?\sAPRESENTAD'
        # # self.regex_anti_quadro = '(((JULG(O|ASE)|DECIDO) (IMPROCEDENTE|PROCEDENTE|EXTINTO) O (PEDIDO|PROCESSO))|(EXPEC(O|ASE) EDITAL.{0,100} RESUMO)|(REJEIT(OU(SE)?) A IMPUGNACAO)|(IMPUGNACAO DE CREDITO)|(ANALISE E ELABORACAO)|(DETERMINO A INCLUSAO DO CREDITO)|(INCLU(ISE|SAO|A|O) (DO)? CREDITO)|(PROVIDENCI(E|AR|OU) O RECOLHIMENTO)|(EXPEDICAO D[OE] MANDADO)|(EXECUCAO EMBARGADA)|(CONSIDERO PREJUDICADO)|(DEVERAO? SER (INCLUIDOS|CONSIDERADOS).{0,100}D(E|OS) CREDORES)|(INCLUSAO .{0,100} QUADRO (GERAL )?DE CREDORES)|(AGUARD(A ?SE|O) A PUBLICACAO DO EDITAL)|(DEVERA .{0,50}HABILITAR O (SEU )?CREDITO)|(CASO HAJA INTEESSE EM CONSTAR [DN]O QUADRO GERAL D(E|OS) CREDORES)|((PUBLIQUE ?SE (O NOVO)?[OA]?|ALTERESE A|DEVERA ELABORAR [OA] NOV[OA]) (RELACAO|QUADRO( GERAL)?|LISTA) D[EO]S? CREDORES)|(VALOR RELATIVO AS?( CUSTAS DE)? PUBLICACAO)|(DEVERA CONTER .{0,50} RELACAO( NOMINAL)? DE CREDORES)|(CADA CARACTERE CONTIDO NO TEXTO (QUE SERA IMPRESSO )?[DN]O EDITAL)|((QUE DEVERA|A) SER RECOLHID[AO] POR GUIA)|(CUSTO DO EDITAL)|((QUE)?( OS? MESMOS?)? PODE(NDO|RAO?)?( OS? MESMOS?)? SER(EM)? IMPUGNAD[OA]S?)|(AGUARD(ASE|O|ANDO) (PEL[OA] REQUERENTE )?A APRESENTACAO (DA MINUTA )?DO EDITAL)|(PEDIDO DE PENHORA)|(ELABORE (QGC|ROL|LISTA|QUADRO|RELACAO|EDITAL(\sDE\sCONVOCACAO)?)( GERAL DE CREDORES)? ATUALIZADO)|(ARBITRAMENTO DOS HONORARIOS DO (SINDICO|ADMINISTRADOR JUDICIAL) EM)|(OS BENS FORAM AVALIADOS EM)|(HOMOLOGO A VENDA)|(DEFIRO A ENTREGA DOS BENS)|(RECEBIMENTO.{0,15} HABILITACAO DE CREDITO)|(DEPOSITO JUDICIAL (REALIZADO POR|NO VALOR DE))|((QUADRO GERAL DE CREDORES|QGC) (DEVIDAMENTE|DEVERA SER) RETIFICADO)|(BEM COMO DEMAIS VERBAS TRABALHISTAS))'
        # self.regex_anti_quadro = '(((?<!\\bCONSTA )(JULG(O|ASE)|DECIDO) (IMPROCEDENTE|PROCEDENTE|EXTINTO) O (PEDIDO|PROCESSO))|((O JULGAMENTO|REJEIT(OU(SE)?)|APRESENT(ARAM|OU)) (D?A )?IMPUGNACAO)|SEGUINTES? PETIC(OES|AO) DE HABILITACAO\s*(E\s*)?IMPUGNACAO DE CREDITO|(SE PRETENDE IMPUGNAR ES[ST]E CREDITO)|(APRESENTADA (UMA )?(IMPUGNACAO|HABILITACAO) DE CREDITO)|(ANALISE E ELABORACAO)|(DETERMIN(O|ANDO) A (INCLUSAO|CORRECAO) DO (VALOR DO )?CREDITO)|(PEDE A INCLUSAO COMO)|(ALEGANDO SER CREDOR)|(INCLU(ISE|SAO|A|O) (DO)? CREDITO)|(PROVIDENCI(E|AR|OU) O RECOLHIMENTO)|(EXPEDICAO D[OE] MANDADO)|(EXECUCAO EMBARGADA)|(CONSIDERO PREJUDICADO)|(DEVERAO? SER (INCLUIDOS|CONSIDERADOS).{0,100}D(E|OS) CREDORES)|(INCLUSAO .{0,100} QUADRO (GERAL )?DE CREDORES)|(AGUARD(A ?SE|O) A PUBLICACAO DO EDITAL)|(DEVERA .{0,50}HABILITAR O (SEU )?CREDITO)|(CASO HAJA INTERESSE EM CONSTAR [DN]O QUADRO GERAL D(E|OS) CREDORES)|((REPUBLIQUE ?SE (O )?|PUBLIQUE ?SE (O )?NOV|ALTERESE |DEVERA ELABORAR [OA] NOV)[OA] (RELACAO|QUADRO( GERAL)?|LISTA) D[EO]S? CREDORES)|(VALOR RELATIVO AS?( CUSTAS DE)? PUBLICACAO)|(DEVERA CONTER .{0,50} RELACAO( NOMINAL)? DE CREDORES)|(CADA CARACTERE CONTIDO NO TEXTO (QUE SERA IMPRESSO )?[DN]O EDITAL)|((QUE DEVERA|A) SER RECOLHID[AO] POR GUIA)|(CUSTO DO EDITAL)|(AGUARD(ASE|O|ANDO) (PEL[OA] REQUERENTE )?A APRESENTACAO (DA MINUTA )?DO EDITAL)|(PEDIDO DE PENHORA)|(ELABORE (QGC|ROL|LISTA|QUADRO|RELACAO|EDITAL(\sDE\sCONVOCACAO)?)( GERAL DE CREDORES)? ATUALIZADO)|(ARBITRAMENTO DOS HONORARIOS DO (SINDICO|ADMINISTRADOR JUDICIAL) EM)|(OS BENS FORAM AVALIADOS EM)|(HOMOLOGO A VENDA)|(DEFIRO A ENTREGA DOS BENS)|(RECEBIMENTO.{0,15} HABILITACAO DE CREDITO)|(DEPOSITO JUDICIAL (REALIZADO POR|NO VALOR DE))|((QUADRO GERAL DE CREDORES|QGC) (DEVIDAMENTE|DEVERA SER) RETIFICADO)|(DEVERA (O AUTOR |SER )?RECOLH(ER|IDA) (NO PRAZO DE \w+ DIAS |A TAXA ((DO )?EDITAL)? )?N?O VALOR)|(SOLICITOU QUE [OA] HABILITANTE)|(QUE (SE )?AGUARDE A PUBLICACAO DO EDITAL PREVISTO ([ND]OS? )?ARTIGOS? 7O ?2O)|(HOMOLOGO OS HONORARIOS)|((INDEFIRO A|NAO HA (A )?NECESSIDADE D[EA]) (RE)?PUBLICACAO DO QUADRO GERAL DE CREDORES)|((IN)?DEFIRO A INDICACAO D[EAO].{0,100}PELO VALOR DE.{0,30}HONORARIOS)|(CUSTO DE PUBLICACAO DO EDITAL REFERENTE A RELACAO DE CREDORES ARTIGO 7 ?2)|(NOMEIO PERITO CONTABIL)|((ARBITRO|DEFINO) (A REMUNERACAO|OS HONORARIOS) D[OA] SINDIC[OA])|(AGUARDANDO PUBLICACAO DE EDITAL DE CONVOCACAO DE CREDORES)|(POR CESSAO DE CREDITO ALTERANDO ?SE (POR CONSEQUENCIA )?OS CREDORES)|(CREDITO JA CONSTA [ND]O QUADRO GERAL DE CREDORES)|(JUNTADA AOS AUTOS DE (HABILITACAO|IMPUGNACAO) DE CREDITO)|(A PRESENTE IMPUGNACAO DE CREDITO)|(SINDICO DECLINOU D?O CARGO)|(TRATASE DE PENHORA)|(PUBLIQUE ?SE( O)? (RELACAO|QUADRO( GERAL)?|LISTA) D[EO]S? CREDORES COMPLEMENTAR))'
    #encontrei um caso que custo do edital aparece no quadro. verificar!
    def __inclui_itens_de_aux_na_lista_principal(self, lista_aux, lista_classes):
        item_auxiliar_esta_na_lista = False
        for item_auxiliar in lista_aux:
            for classe in lista_classes:
                item_auxiliar_esta_na_lista = False
                if (item_auxiliar.start() >= classe.start() and item_auxiliar.end() <= classe.end()): #se o auxiliar está contido na classe
                    item_auxiliar_esta_na_lista = True
                    break
                elif item_auxiliar.group(0).strip() != classe.group(0).strip() and item_auxiliar.start() <= classe.start() and item_auxiliar.end() >= classe.end(): #se a classe está contida no auxiliar, trocar
                    item_auxiliar_esta_na_lista = True
                    lista_classes.remove(classe)
                    lista_classes.append(item_auxiliar)
            if not item_auxiliar_esta_na_lista:
                lista_classes.append(item_auxiliar)

    def _regex_findall(self, regex, texto, retorno):
        retorno.extend(regex.findall(texto))

    def aplica_regex_com_timeout(self, regex, texto, retorno, timeout=200):
        p = Process(target=self._regex_findall, args=(regex, texto, retorno))
        try:
            p.start()
            p.join(timeout)
        finally:
            p.terminate()
            del p

    # return regex.findall(texto)
    def verifica_quadro_credores(self, texto, data, processo, caderno=None, fonte_dado='DJSP', movimento=None, debug=True, blocoQuadro=None):
        i = 0
        #EDIÇÕES ESPECÍFICAS PARA DETERMINADO QUADRO
        # texto = re.sub(' +\d+ +',' ',texto)
        # texto = re.sub('([A-Z]+)\s+(\d+)','\g<1>, \g<2>',texto)
        # texto = re.sub(' \d+\/\d+ ',' ',texto)
        # texto = re.sub('\s*(\d{3}\.?\d{3}\.?\d{3}(-\d{2})?|\d{1,2}\.\d{3}\.\d{3}\.\d{3}|\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}|NAO LOCALIZADO)\s.*?\s(\d{5}-\d{3}|\d{6,8}|\d{2}\.\d{3}-\d{3})',', ',texto)
        texto = re.sub('\s*NOME\s*-\s*VALOR\s*R\$:\s*',' ',texto)
        # texto = re.sub('ESTE DOCUMENTO E COPIA DO ORIGINAL.*?INFORME O PROCESSO E CODIGO\s*\w+\.\s*ORDEM NOME DO CREDOR CNPJ\/CPF\/OAB VALOR ','',texto)
        blocoQuadroService = BlocoQuadroService()
        classeCredorService = ClasseCredorService()
        credorService = QuadroCredorService()

        texto_movimento = RegexUtil.limpa_texto_para_movimento_e_diario_para_quadro_credor(remove_acentos(texto))
        #ESSA LIMPEZA DEVE SER FEITA Após a limpeza do diário e do movimento, não retirar daqui.
        texto_movimento = re.sub('\d{1,2}\sDE\s(JANEIRO|FEVEREIRO|MARÇO|ABRIL|MAIO|JUNHO|JULHO|AGOSTO|SETEMBRO|OUTUBRO|NOVEMBRO|DEZEMBRO)\sDE\s\d\.?\d{3}','',texto_movimento)

        if debug:
            print(texto_movimento)
        # REGEX 1 (TODOS QUE COMEÇAM COM CLASSE (I,II,III…)(:-)
        expressao_classe_romanos = re.compile("((CLASSE\s(IV|I{1,3}|VI{0,3}))\s?)[:\s-]?[\s]?(CRED(ITOS?|OR(ES)?))?[:\s-]?(TRABALHISTAS?|(SUB)?QUIROGRAFARI[OA]S?|(COM)?\s?GARANTIA\sREAL|EXTRACONCURSA(L|IS)?|TRIBUTARIOS?|PRIVILEGIADOS?|APURADOS?|COM\sPRIVILEGIOS?\s?(ESPECIA(IS|L)|GERA(IS|L))?|POR\sRESTITUICAO?|ENCARGOS?\sDA\sMASSA|SUBORDINADOS?)?[\s:]*(\((ATIVOS?\|BANCOS|\(INSS\)|(\(FAZENDA\s(NACIONAL|MUNICIPAL|ESTADUAL))\)|PREFERENCIA(L|IS)|FORNECEDORES)\))?[\s:]?-?\s?")

        # REGEX 2 começam com (CREDITOS(ORES,ITO) “NOME DA CLASSE)
        expressao_classe_creditos = re.compile("((TOTAL (GERAL )?D[OE]S? )?CRED(ITOS?|OR(ES)?))[\s-]?\s?(NAO|COM\s|POR\s|(^\()CUSTAS\s|NA\sFORMA\s)?(SUB[\s]?TOTAL|(PREVIDENCIARIOS\sE\s)?TRIBUTARI[OA]S?|BANCARIO[S]?|PRIVILEGI(AD[AO]|[O])S?\s?(GERAL|FISCA(IS|L)|ESPECIAL)?|PROCESSUAIS(^\))|FISCO[-\s]*(TRIBUTARI[OA]S?)?|TRABALHISTAS?|(SUB)?\-?QUIROGRAFARI[OA]S?|RESTITUIC(AO|OES)?|EXTRACONCURSA(L|IS)|(FISCAL\s?)|(SUB[\s-]?)|(COM)?\s?GARANTIA\sREAL|FISCA(IS|L)\s?(\-?\s?FISCAL)?)\s?((NAO)?\s?\(?FORNECEDOR(ES\)?)?|\(ATIVOS\)|\(?BANCOS\)?|TEMPESTIVOS?|TRABALHISTAS?|\(INSS\)|(\(FAZENDA\s(NACIONAL|MUNICIPAL|ESTADUAL))\))?.{0,5}?[:\-][\s]?((CLASSE\s(IV|I{1,3}|VI{0,3}))\s?)?")

        # REGEX 3 - Regex para pegar declarações do tipo: II - QUIROGRAFARIOS

        expressao_classe_nome = re.compile("(\\b)((IV|I{1,3}|VI{0,3})[:\s-]*)?(((TOTAL\s?( GERAL)?( DE)?|LL?ISTA|SEGUINTES?|RELACAO|RESERVA|ROL)\s?(DE)?\s?CRED(ITOS|ORES|OR|ITO)\s?(PELA\sFALIDA)?)|EXTRACONCURSAL|TRABALHISTA[S]?|TRIBUTARIO|PRIVILEGI(AD[AO]|[O])S?s?\s?(FISCAL|ESPECIAL|TRABALHISTA)?|FORNECEDO(R|RES)|FISCAL|(COM)?[\s]?GARANTIA\s?(REAL)?|(FORNECEDORES\s(NACIONAIS)?|INSTITUICOES\sFINANCEIRAS))(\s)?(FORNECEDORES\s(NACIONAIS)?|INSTITUICOES\sFINANCEIRAS)?[:\-\?]|INTERCOMPANY\)?:|(DIVIDA|QUIROGRAFARIO)S?\s*INTERCOMPANY")

        # REGEX 4: Regex que já começa com o nome da classe  ex: TRABALHISTA:
        # expressao_classe_total_subtotal = re.compile("((SUB)?[\s]?TOTAL.{0,30}?)[:\s]?(GERAL[\s:])?(DE)?\s?(DOS?)?[\s]?(CRED(ITOS?|OR(ES)?))?[\s]?((CLASSE\s(I{1,3}|IV|VI{0,3}))\s?)?[:\-\s]*(CRED(ITOS?|OR(ES)?))?[\s]?((SUB[\s\-:\?])?QUIROGRAFARI[OA]S?|PASSIVOS?|TRABALHISTAS?|(COM)?[\s]?GARANTIA\sREAL|EXTRACONCURSA(IS|L)|TRIBUTARIOS?|PASSIVOS?\s(TRIBUTARIOS?)?|PRIVILEGIADOS?|APURADO|COM\sPRIVILEGIOS?\s(ESPECIA(L|IS)|GERA(L|IS))|POR\sRESTITUICAO|ENCARGOS?\sDA\sMASSA)?[[\s]?[-=:\s]?")
        # expressao_classe_total_subtotal = re.compile("((SUB)?[\s]?TOTAL.{0,30}])[:\s]?(GERAL[\s:])?(DE)?\s?(DO[S])?[\s]?(CRED(ITOS|ORES|OR|ITO))?[\s]?((CLASSE\s(I{1,3}|IV|VI{0,3}))\s?)?[:\-\s]*(CRED(ITOS|ORES|OR|ITO))?[\s]?((SUB[\s\-:\?])?QUIROGRAFARI[OA][S]?|PASSIVOS?|TRABALHISTA[S]?|(COM)?[\s]?GARANTIA\sREAL|EXTRACONCURSAIS|TRIBUTARIO[S]?|PASSIVO/s(TRIBUTARIO)?|PRIVILEGIADO[S]?|APURADO|COM\sPRIVILEGIO\s(ESPECIAL|GERAL)|POR\sRESTITUICAO|ENCARGOS\sDA\sMASSA)?[[\s]?[-=:\s]?")

        expressao_novas_classes = re.compile('(TOTAL\s|BANCOS?\s|CREDOR(ES)?\s?)?(\\b)((APRESENTOU\sO\sQUADRO\sGERAL\sABAIXO|CRED(ITO|ORE)S\s(COM\sDIREITOS\sREAIS\sDE\sGARANTIAS?|D[AO]\s(M(\.?|ASSA)?\s?)?FALID[AO])|(LISTA|RELACAO|ROL|QUADRO(\sGERAL)?)\s(NOMINAL\s*)?(D(E|OS)\sCREDORES(\sAPRESENTAD[AO]|\sATUALIZAD[AO]|\sHOMOLOGAD[AO]|\sCONVOCAD[OA]S?)?|NOMINATIVA\sDOS\sCREDORES\s(NAO\s)?SUJEITOS\sAOS\sEFEITOS\sDA\sCONCORDATA)|TRABALHISTAS?|(SUB)?[QO]UIRO\w*GRAF(ARI[OA][S]?|ICO)|RESTITUIC(OES|AO)|HABILITAC(OES|AO) DE CREDITOS?|((CREDORES )?COM)?\s?GARANTIA\sREAL|EXTRACONCURSA(L|IS)?|TRIBUTARIO[S]?|PREFERENCIA(L|IS)|DERIVADOS?\sDA LEGISLACAO\sDO\sTRABALHO|IMPOSTOS\sE\sTAXAS\sA\sPAGAR|PRIVILEGIADO[S]?|(CREDORES )?COM\sPRIVILEGIO\s?(ESPECIAL|GERAL)?|POR\sRESTITUICAO?|ENCARGOS\sDA\sMASSA|SUBORDINADOS|ACC|PENHORA?|PEDIDO\sDE\sRESERVA|DEBITOS FISCAIS|FORNECEDORES\s?((INTER)?NACIONA(IS|L))?|CONTAS\sA\sPAGAR|MULTAS?\s*:)\\b[\.\s:]*?[^\?,A-Z]|((EMPRESTIMOS?(\/FINANCIAMENTOS?)?|BANCOS?)\\b\s*\:))(\(?(FORNECEDOR(ES)?|ATIVOS|BANCOS|\(INSS\)|(\(FAZENDA\s(NACIONAL|MUNICIPAL|ESTADUAL))\)|PREFERENCIA(L|IS)|FISCA(IS|L)|TRABALHISTAS?|GERAL(\sDE\sCREDORES)?|CONTAS?\s?(ESPECIA(L|IS))?|E\sFACTORINGS?|CAPITAL\sDE\sGIRO|GERA(L|IS))\)?|DOS\sDEBITOS|PEL[OA]S?\s(FALID[OA]S?|ADMINISTRADORA?(\sJUDICIAL)?|SINDIC[OA]))?[\s:]*-?\s?')
        # expressao_novas_classes = re.compile('(TOTAL\s|BANCOS?\s)?(APRESENTOU\sO\sQUADRO\sGERAL\sABAIXO|CREDITOS\sCOM\sDIREITOS\sREAIS\sDE\sGARANTIAS?|(RELACAO|ROL|QUADRO(\sGERAL)?)\sD(E|OS)\sCREDORES(\sAPRESENTAD[AO]|\sATUALIZAD[AO]|\sHOMOLOGAD[AO])?|TRABALHISTAS?|(SUB)?QUIRO\w*GRAF(ARI[OA][S]?|ICO)|(COM)?\s?GARANTIA\sREAL|EXTRACONCURSA(L|IS)?|TRIBUTARIO[S]?|PRIVILEGIADO[S]?|COM\sPRIVILEGIO\s?(ESPECIAL|GERAL)?|POR\sRESTITUICAO?|ENCARGOS\sDA\sMASSA|SUBORDINADOS|FORNECEDORES\s?((INTER)?NACIONA(IS|L))?|EMPRESTIMO|CONTAS\sA\sPAGAR|MULTAS?:)[\.\s:]*(\(?(ATIVOS|BANCOS|\(INSS\)|(\(FAZENDA\s(NACIONAL|MUNICIPAL|ESTADUAL))\)|PREFERENCIA(L|IS)|FISCA(IS|L)|TRABALHISTAS?|GERAL(\sDE\sCREDORES)?|CONTAS?\s?(ESPECIA(L|IS))?|E\sFACTORINGS?|CAPITAL\sDE\sGIRO)\)?|DOS\sDEBITOS|PEL[OA]S?\s(FALID[OA]S?|ADMINISTRADORA?(\sJUDICIAL)?|SINDIC[OA]))?[\s:]*-?\s?')

        # NOMES E VALORES:

        expressao_quadro_simples_moeda_obrigatoria = re.compile('(^|[;\.,\-\s]|\\b)([A-Z].*?[\w\.,\-\s\?]{1,4})(VALOR)?\s*((\\b(R?[\£\€\$\¥]|USD|BRL|US\$|EUR|GBP|JPY|CHF|CLP|NOK|SEK)\s*(\d[\.,;]?)+[\.,;]\d{2}\\b\s*E?\s*)+)')  # group2 nome, group 4 valor
        expressao_quadro_simples = re.compile('(^|[;\.,\-\s]|\\b)([A-Z].*?[\w\.,\-\s\?]{1,4})\s*(VALOR[\.,\-\s\?]+)?((R?[\£\€\$\¥]?\s*(\d[\.,;]?)+[\.,;]\d{2}\\b\s*E?\s*)+)')  # group2 nome, group 4 valor

        expressao_quadro_subtracao_valor_final = re.compile('(\s|^|\\b)([A-Z].*?)[,\-\s]+(.{0,4}\$?(\d[\.,;]?)+,\d{2})+\s\-(.{0,4}[\£\€\$\¥]?(\d[\.,;]?)+,\d{2})+\s\=(.{0,4}\$?(\d[.,;]?)+,\d{2}\\b)+')
        expressao_quadro_nome_cnpj_valor = re.compile('(((\s|^|\\b)([A-Z].*?)[\.,\-\s\?\:\;]*))[\.,\-\?\:\;\s]*?(((CNPJ|CPF)?\s?(NO)?\s?)(\d{2}\.?\d{3}\.?\d{3}\/?\d{4}\-?\d{2}|\d{3}\.?\d{3}\.?\d{3}\-?\d{2})[\.,\-\?\s]*)?((\\b(\D{0,2}?[\£\€\$\¥]|\D{0,3}?)\s*?(\d[\.,;]?)+?[\.,;]\s*\d{2}\\b\s*?E?\s*?))+?') #group 2 nome, group 5 cnpj group 9 valor
        expressao_quadro_com_valor_com_casas_decimais_erradas = re.compile('(^|[;\.,\-\s]|\\b)([A-Z].*?[\w\.,\-\s\?]{1,4}?)(VALOR)?((\\b(R\$|[\£\€\¥]|USD|BRL|US\$|EUR|GBP|JPY|CHF|CLP|NOK|SEK|\$)\s*:?\s*(\d[\.,;]?)+[\.,;]?\d{0,2}\\b\s*E?\s*)+)') #group 2 nome, group 5 moeda
        # Lista Aux é temporária e sobrescrita
        lista_classes = list(expressao_novas_classes.finditer(texto_movimento))
        lista_aux = list(expressao_classe_romanos.finditer(texto_movimento))
        self.__inclui_itens_de_aux_na_lista_principal(lista_aux, lista_classes)
        lista_aux = list(expressao_classe_creditos.finditer(texto_movimento))
        self.__inclui_itens_de_aux_na_lista_principal(lista_aux, lista_classes)
        lista_aux = list(expressao_classe_nome.finditer(texto_movimento))
        self.__inclui_itens_de_aux_na_lista_principal(lista_aux, lista_classes)
        # lista_aux = list(expressao_classe_total_subtotal.finditer(texto_movimento))
        self.__inclui_itens_de_aux_na_lista_principal(lista_aux, lista_classes)
        lista_classes = list(set(lista_classes))
        lista_classes = sorted(lista_classes, key= lambda match: match.start())
        if len(lista_classes) != 0:
           # ConfigManager().escreve_log("Não achou a classe ainda! Verificar se tem erro. Texto: {}".format(texto_movimento), "DJSP", "erros_quadro_credores.txt")
        # else:
            map_classes_credores = {}
            i = 0
            while (i < len(lista_classes)):
                classe = texto_movimento[lista_classes[i].start():lista_classes[i].end()].strip().strip('-:')
                fim_dos_credores_da_classe = lista_classes[i + 1].start() if i + 1 < len(lista_classes) else None
                if classe in list(map_classes_credores.keys()):
                    map_classes_credores.update({classe: map_classes_credores[classe]+' '+texto_movimento[lista_classes[i].end():fim_dos_credores_da_classe].strip()})
                else:
                    map_classes_credores.update({classe: texto_movimento[lista_classes[i].end():fim_dos_credores_da_classe].strip()})
                i+=1

            #print(10*"#" + " Quadro de credores do processo: NPU {} - ID {} ".format(processo.npu,processo.id) + 10*"#")
            for classe,valor in sorted(map_classes_credores.items()):
                posicao_moeda = 9
                usou_regex_casa_decimal_errada = False
                valor = re.sub('(\.\s){2,}','.',valor)
                manager = Manager()
                match_quadro = manager.list()
                self.aplica_regex_com_timeout(expressao_quadro_nome_cnpj_valor,valor,match_quadro)
                if not match_quadro or len(match_quadro) == 0 or self.moeda_no_nome_credor(match_quadro):
                    posicao_moeda = 3
                    match_quadro = manager.list()
                    self.aplica_regex_com_timeout(expressao_quadro_subtracao_valor_final,valor,match_quadro)
                    if not match_quadro or len(match_quadro) == 0 or self.moeda_no_nome_credor(match_quadro):
                        posicao_moeda = 4
                        match_quadro = manager.list()
                        self.aplica_regex_com_timeout(expressao_quadro_simples_moeda_obrigatoria,valor,match_quadro)
                        if not match_quadro or len(match_quadro) == 0 or self.moeda_no_nome_credor(match_quadro):
                            match_quadro = manager.list()
                            self.aplica_regex_com_timeout(expressao_quadro_simples,valor, match_quadro)
                            if not match_quadro or len(match_quadro) == 0 or self.moeda_no_nome_credor(match_quadro):
                                match_quadro = manager.list()
                                self.aplica_regex_com_timeout(expressao_quadro_com_valor_com_casas_decimais_erradas, valor, match_quadro)
                                usou_regex_casa_decimal_errada = True
                #(' ', 'BANCO BRADESCO S/A', '', 'R$90.651,57', 'R$90.651,57', '1')
                if match_quadro and len(match_quadro) > 0:
                    classeCredor = classeCredorService.preenche_classe_credor(classe)
                    if not blocoQuadro:
                        blocoQuadro = blocoQuadroService.preenche_bloco_quadro(texto, texto_movimento, movimento, caderno)
                    for item_quadro in sorted(match_quadro):
                        # if 'CLASSE III' in item_quadro[1].strip().upper():
                        #     print('ACHOU!')
                        total = {}
                        nome_credor_cortado = '' #esta variável serve para casos como o if abaixo, as vezes ele detect SA como tipo_moeda e retira esta parte do nome do credor. essa variável então corrige o problema

                        #CORREÇÃO NECESSARIA PARA CASOS EM QUE NAO TEM NOME DO CREDOR. ELE SEPARAVA O VALOR E COLOCAVA PARTE COMO NOME DO CREDOR.
                        if item_quadro[1].strip().startswith('R$'):
                            acertando_valor = 'R$'
                            for char in item_quadro[1].strip()[2:]:
                                if char.isdigit():
                                    acertando_valor+=char
                                else:
                                    break
                            item_quadro = list(item_quadro)
                            item_quadro[posicao_moeda] = acertando_valor + item_quadro[posicao_moeda]
                            item_quadro[1] = item_quadro[1].replace(acertando_valor,'',1)

                        for valor in re.finditer('([^0-9\s]+)?\s*([0-9\.\,\s]+)', item_quadro[posicao_moeda].strip()):
                            moeda = valor.group(1)
                            if not moeda:
                                moeda = 'R$'
                            else:
                                moeda = re.sub('[,;\\\"\'\.\-\/\?\!\—\–\)\(\s\[\]\:\*]', '', moeda)
                                if moeda.strip() in (
                                        'A', 'L', 'E', 'D', 'S', 'C', 'M', 'R', 'J', 'F', 'N', 'P', 'O', 'B', 'SA',
                                        'DE', 'LT',
                                        'EPP', 'LTDA', 'LTD', 'MEI', 'ME', 'LT' 'A*', 'E*', 'NO:', 'NO', 'SP', 'SC',
                                        'RJ', 'DA',
                                        'AS', 'JR', 'EM', '*', '**', '***', 'VAZ', 'LUZ', 'CEP', 'AG', 'A*', 'SI',
                                        'COM', 'II',
                                        'I', 'V', 'AP', 'DOI', 'RS', ' SO', 'PAZ', 'MG', 'DF', 'PE', 'SUL', 'GO', 'AB',
                                        'CIA',
                                        'AL', 'FE', 'REI', 'JE', 'BR', 'PR', 'RO', 'BA', 'DIA', 'SIL', 'CPF', 'IND',
                                        'SO', 'EP',
                                        'DO', 'CO', 'FO', 'LE', 'DAS', 'VI', 'CP', 'ABE', 'FI', 'CDA'):
                                    if not moeda in nome_credor_cortado:
                                        nome_credor_cortado = nome_credor_cortado + ' ' + moeda
                                    moeda = 'R$'
                                # else:
                                    # moeda = valor.group(1).strip()
                            quantia_bruta = valor.group(2).strip()
                            quantia = 0

                            if not usou_regex_casa_decimal_errada:
                                if '.' in quantia_bruta or ',' in quantia_bruta or ' ' in quantia_bruta:
                                    digitos = sum(d.isdigit() for d in quantia_bruta)
                                    pontos = sum(p=='.' or p == ',' for p in quantia_bruta)
                                    digitos_por_ponto = digitos // pontos #precisei fazer isso pois casos como 02,01,12,123,21,04,02 ele achava que era dinheiro
                                    if 3 <= digitos_por_ponto:
                                        quantia_bruta = quantia_bruta.replace(',', '').replace('.', '').replace(' ','')
                                    else:
                                        quantia_bruta = ''
                                    if quantia_bruta != '':
                                        quantia = Decimal(quantia_bruta[:-2] + "." +
                                                          quantia_bruta[-2:]).quantize(Decimal('0.01'),
                                                                                       rounding=ROUND_HALF_EVEN)
                            else:
                                quantia_bruta = quantia_bruta.replace('.', '').replace(' ', '')
                                if quantia_bruta.endswith(','):
                                    quantia_bruta = quantia_bruta[:-1]
                                if ',' in quantia_bruta:
                                    if len(quantia_bruta[quantia_bruta.find(',')+1:]) < 2:
                                        while len(quantia_bruta[quantia_bruta.find(',')+1:]) < 2:
                                            quantia_bruta+='0'
                                    else:
                                        while ',' in quantia_bruta and len(quantia_bruta[quantia_bruta.find(',') + 1:]) > 2:
                                            quantia_bruta = quantia_bruta.replace(',', '',1)
                                else:
                                    quantia_bruta+='.00'
                                quantia_bruta = quantia_bruta.replace(',','.')
                                quantia = Decimal(quantia_bruta).quantize(Decimal('0.01'),rounding=ROUND_HALF_EVEN)

                            if moeda not in total.keys():
                                total[moeda] = 0

                            total[moeda] += quantia


                        # classeCredor = classeCredorService.preenche_classe_credor(classe)

                        tipo_moeda = list(total.keys())[0]
                        nome_credor = item_quadro[1].strip() + " " +  nome_credor_cortado.strip()
                        if len(tipo_moeda) > 1 and tipo_moeda.startswith(',') and not any( tipo_moeda == moeda for moeda in ['BRL','USD','R$','US$', 'U$','EUR','£','GBP','€','¥', 'JPY', 'CHF', 'CLP','NOK', 'SEK']): #,brlas.dsa.d.
                            nome_credor = nome_credor+ tipo_moeda.strip().upper()
                            tipo_moeda = ''
                        tipo_moeda = re.sub('[,;\\\"\'\.\-\/\?\!\—\–\)\(\s\[\]\:\*]', '',tipo_moeda)
                        if tipo_moeda.strip() == '':
                            tipo_moeda = 'R$'
                        valor = total[list(total.keys())[0]]
                        if valor > 0:
                            credor = credorService.preenche_quadro_credor(
                                    processo, nome_credor, data,
                                    tipo_moeda, valor, classeCredor,fonte_dado,self.tag,blocoQuadro)
                            if debug:
                                ConfigManager().escreve_log('{} : {} : {} ({})'.format(classeCredor.nome, credor.nome,item_quadro[posicao_moeda],
                                                             credor.tipo_moeda + " " + str(credor.valor)),'DJSP','quadro_teste_verificar_erro.txt')

                        i+=1

            credorService.dao.commit()
            if debug:
                print(10 * "#" + " Fim do quadro " + 10 * "#")
        else:
            print(30 * "*" + " QUADRO DO PROCESSO {} NAO ENCONTRADO ".format(processo.npu_ou_num_processo) + 30 * "*")


    def moeda_no_nome_credor(self, match_quadro):
        tipo_moeda_e_numero = re.compile('\\bR?[\£\€\$\¥]\s*:?\s*\d')
        for item_quadro in list(match_quadro):
            if tipo_moeda_e_numero.search(item_quadro[1]):
                return True
        return False

    #aqui devo fazer verificações pequenas, como a query para encontrar possíveis quadros. caso tenha, chamar o método de baixo
    def verifica_possibilidade_de_quadro(self, texto):
        if not texto:
            return False
        match = (re.search(RegexUtil.regex_moedas,texto, re.IGNORECASE) and 'CREDOR' in texto.upper()) \
            and (((re.search(RegexUtil.regex_quadro_artigo,texto, re.IGNORECASE)) and not re.search(RegexUtil.regex_anti_quadro,texto,re.IGNORECASE))
        or (re.search(RegexUtil.regex_quadro_prioritario,texto, re.IGNORECASE)))

        return True if match else False
            # or re.search(self.regex_quadro_sem_classe,texto, re.IGNORECASE))
            # and (not re.search(self.regex_quadro_excluir_encerramento,texto, re.IGNORECASE)
            # or re.search(self.regex_quadro_indicacao_relacao,texto, re.IGNORECASE))

    def verifica_quadro_credores_no_diario(self,texto,data, processo, caderno=None,fonte_dado='DJSP', movimento=None):
        texto_diario = RegexUtil.limpa_texto_para_movimento_e_diario_para_quadro_credor(remove_acentos(texto))
        texto_diario = remove_varios_espacos(texto_diario)
        #Limpeza do que é referente apenas ao texto do diário
        texto_diario = RegexUtil.limpa_texto_diario_para_quadro_credor(texto_diario)
        self.verifica_quadro_credores(texto_diario, data, processo,caderno=caderno,fonte_dado=fonte_dado,movimento=movimento)

    def cria_quadros_a_partir_do_bloco(self, bloco, processo=None, data=None):

        if not processo:
            processos = []
            for quadro_credor in bloco.quadro_credores:
                if quadro_credor.processo not in processos:
                    processos.append(quadro_credor.processo)
            processos = list(set(processos))
            print('Existem {} processos para o bloco {}'.format(len(processos), bloco.id))
            for processo in processos:
                self.verifica_quadro_credores(bloco.texto, data,processo,bloco.caderno,'DJSP' if bloco.caderno is not None else 'MOVIMENTO - SAJ',bloco.movimento,blocoQuadro=bloco)
        else:
           self.verifica_quadro_credores(bloco.texto, data, processo, bloco.caderno,'DJSP' if bloco.caderno is not None else 'MOVIMENTO - SAJ', bloco.movimento, blocoQuadro=bloco)

    def acerta_nome_credor(self, regex_substituicao, string_substituicao=''):
       quadroCredorService = QuadroCredorService()
       anti_regex = re.compile('TOTAL')
       quadros_credores = quadroCredorService.dao.get_credores_que_precisam_ser_corrigidos(regex_substituicao)

       for quadro_credor in quadros_credores:

           if len(quadro_credor.nome) < 250 and len(quadro_credor.nome) > 4 and quadro_credor.nome is not None:
               if not re.search(anti_regex, quadro_credor.nome):
                   print('Nome antigo: ', quadro_credor.nome)
                   # quadro_credor.nome = re.sub('PUBLICACAO OFI\s?CIAL DO TRIBUNAL DE JUSTICA DO ESTADO DE SAO PAULO LEI O (\d*)?\s?(VALOR)?','',quadro_credor.nome)
                   quadro_credor.nome = re.sub(regex_substituicao, string_substituicao, quadro_credor.nome)
                   print(quadro_credor.id, quadro_credor.nome)
                   if len(quadro_credor.nome) > 4:
                       quadroCredorService.salvar(obj=quadro_credor, tag='FALENCIAS')

if __name__ == '__main__':

    bloco_quadro_service = BlocoQuadroService()
    processo_service = ProcessoService()
    classificaQuadro = ClassificaQuadroCredores(tag='FALENCIAS')

    if len(sys.argv) == 3:
        rank = int(sys.argv[1])
        fatia = int(sys.argv[2])
    else:
        rank = 0
        fatia = 1

    #LISTA DE TUPLA QUE CONTÉM O BLOCO_QUADRO_ID, PROCESSO_ID E DATA DO QUADRO. PARA RODAR, PODE ADICIONAR VÁRIOS... eX: [(B,P,D),(B1,P1,D1),....]
    ids = [( 226715	,18322,	'2014-02-28'),
           (339012	,18314,	'2017-03-14'),
           (259553	,18394,	'2016-12-02')]

    print("Rank {}, fatia {}".format(rank, fatia))
    # ultimos_ids = [3585, 3691, 3857, 3115, 3618, 3709, 3785, 3591, 4087, 3668, 3789, 3625, 3911, 3732, 3598, 3884]
    comeca_processamento = True
    for  proc_id, id, data in ids:
        bloco_id = int(id)
        # if bloco_id in problemas:
        processo_id = int(proc_id)
        if bloco_id % fatia == rank:
            if comeca_processamento:
                print(bloco_id)
                bloco = bloco_quadro_service.dao.get_por_id(bloco_id)
                processo = processo_service.dao.get_por_id(processo_id)
                classificaQuadro.cria_quadros_a_partir_do_bloco(bloco, processo, data)
    # qc id '2417132'

    # classificaQuadro = ClassificaQuadroCredores(tag='FALENCIAS')

    #
    # lista_de_ids = ['6017362', '66939905' , '68893147', '72679628']
    # movimentos = movimento_service.dao.listar_por_lista_de_id(rank=rank,fatia=fatia,lista_ids=lista_de_ids)

    #ATENCAO: AQUI EMBAIXO VOCÊS MANDAM EXECUTAR OS POSSIVEIS QUADROS QUE AINDA NÃO RODAMOS
    movimento_service = MovimentoService()
    movimentos = movimento_service.dao.listar_possiveis_quadro_credores(rank=rank,fatia=fatia)
    movimentos_processados = []
    quadro_service = QuadroCredorService()
    for movimento in list(set(movimentos)):
        if not movimento.id in movimentos_processados:
            movimentos_processados.append(movimento.id)
            quadro = quadro_service.dao.get_credores_por_data(movimento.processo,movimento.data)
            if not quadro:
                if classificaQuadro.verifica_possibilidade_de_quadro(movimento.texto):
                    classificaQuadro.verifica_quadro_credores_no_diario(movimento.texto, movimento.data, movimento.processo, caderno=None, fonte_dado='MOVIMENTO - SAJ',movimento=movimento)
                else:
                    print('Não aparenta ser quadro.')
            else:
                print('Quadro {} já inserido'.format(movimento.processo.npu_ou_num_processo))

        else:
            print('Pulando Movimento {}'.format(movimento.processo.npu_ou_num_processo))

        if(len(movimentos_processados) > 10000):
            del movimentos_processados[0]
