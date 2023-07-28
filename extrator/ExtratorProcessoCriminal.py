import re

class ExtratorProcessoCriminal:
    def run(self, arquivo):
        resumo = self.cria_lista_de_linhas(arquivo)
        self.procura_processos_criminal(resumo)

    def tratamento(self, texto):
        if texto:
            texto = texto.group(0)
        else:
            texto = None
        return texto

    def cria_lista_de_linhas_removendo_separador(self, lista_expressoes_ignoradas, separador, arquivo):
        linhas = ''.join(arquivo).split('\n')
        linhas = list(map(lambda linha: re.sub('^\s+', '', linha), linhas))
        linhas = list(filter(lambda linha: linha != '', linhas))
        linhas = list(map(lambda linha: linha + ' SEPARADOR_SEGUNDO_RR ', linhas))

        linhas_concatenadas = ' '.join(linhas)
        for expressao_ignorada in lista_expressoes_ignoradas:
            linhas_concatenadas = expressao_ignorada.sub('', linhas_concatenadas)

        lista_de_linhas = re.split(separador, linhas_concatenadas)
        lista_de_linhas = list(filter(lambda linha: linha.strip() != '', lista_de_linhas))
        lista_de_linhas = list(map(lambda linha: re.sub('\sSEPARADOR_SEGUNDO_RR\s', ' ', linha), lista_de_linhas))

        return lista_de_linhas

    def cria_lista_de_linhas(self, arquivo):
        expressao_cabecalho1 = re.compile(r'((Boa\s*Vista\.)?(\s*\d{1,2}\s*de\s*\w*\sde\s\d{4})?(\s*Diário\s*da\s*Justiça\s*Eletrônico\s*)(ANO\s*\w{2,5}\s*.\s*EDIÇÃO\s*\d{2,5}\s*\d{2,4}\/\d{2,4}))')
        expressao_cabecalho2 = re.compile(r'(\s*Diário\s*da\s*Justiça\s*Eletrônico\s*)(ANO\s*\w{2,4}\s*.\s*EDIÇÃO\s*\d{2,5}\s*\d{2,4}\/\d{2,4})')
        expressao_cabecalho3 = re.compile(r'((Diário\sdo\sPoder\s(Judiciário|Judicário))\s*((ANO|Ano)\s*\w{2,4}\s*.\s*EDIÇÃO\s*\d{3,5})\s*(Boa\s*Vista\-RR)\,.)')
        expressao_data = re.compile(r"\s*\d{1,2}\s*de\s*[A-Za-zÇç]*\s*de\s*20[01]\d")

        lista_expressoes_ignoradas = [
            expressao_cabecalho1,
            expressao_cabecalho2,
            expressao_cabecalho3,
            expressao_data
        ]

        expressao_padrao = re.compile(r'(VARA CRIMINAL[\s\S]*?TRIBUNAL REGIONAL ELEITORAL DE RORAIMA – TRE/RR)', re.IGNORECASE)
        texto = " ".join(arquivo)
        blocos_de_texto = expressao_padrao.findall(texto)

        linhas_concatenadas = ' '.join(blocos_de_texto)
        for expressao_ignorada in lista_expressoes_ignoradas:
            linhas_concatenadas = expressao_ignorada.sub('', linhas_concatenadas)

        separador = re.compile(r'(?:\s+SEPARADOR_SEGUNDO_RR\s+(?:PROC\.?(?:ESSO)?\s*(?:N.)?\s*\:?|\s*N.)?\s*)?'
                               r'(\d{4}.\d{2}.\d{2}.\d{6}\-\d)|'
                               r'(\d{3}.\d{3}.\d\/\d)|'
                               r'(\d{6,7}.\d\/\d{1,2})|'
                               r'(\d{7}\-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4})|'
                               r'(\d{3}\.\d{2}\.\d{6}\-\d)|'
                               r'(\d{8}.\d\/\d.\d{4}\-\d{3})|'
                               r'(\d{3}\.\d{2}\.\d{4}\.\d{6}\-\d(\/?\d{6}\-?\d{3})?)|'
                               r'(\d{3}.\d{2}.\d{5,6}\-\d)|'
                               r'(\d{15}\-\d)|'
                               r'(\d{3,8}\s*.\s *\d{7}.\d{2}.\d{4}.8.23.\d{4})|'
                               r'(\d{3,8}\s*.\d{12}823\d{4})|'
                               r'(\s\d{3,6}\s*.\s*\d{12}\-\d)|'
                               r'(\s+.\s\d{11}.\d)|'
                               r'(\d{4}.\d{2}.\d{6}.\d)|'
                               r'(\d{7}\-\d{2}\.\d{4}\.\d\.?\d{2}\.\d{4})|'
                               r'(\d{3}\.\d{2}\.\d{4}\.\d{6}(\-\d\/\d{6}\-\d{3})?)|'
                               r'(\d{3}\s\d{2}\s\d{6}\s?\-?\d)|'
                               r'(\d{4}.\d{2}.\d?.\d{5}\-\d)|'
                               r'(\d{4}.\d{2}.\d{4}.\d{2}\-\d)|'
                               r'(\s\d{4}.\d{2}.\d{6}\-\d)|'
                               r'(\s\d{12}\s?\-\d)')

        lista_de_linhas = self.cria_lista_de_linhas_removendo_separador(lista_expressoes_ignoradas, separador, linhas_concatenadas)
        return lista_de_linhas

    def procura_processos_criminal(self, lista_de_linhas):
        nao_pegar = re.compile('((Identidade ou Certidão de Nascimento)|(da ))')
        expressao_npu_numero_proc = re.compile('((Processo\sn.\s.{15,16})|(Processo\sn..*\:.{20})|(PROC.\s(N|n).\s.{11,13})|(processo\s*de\s*n.\..{10,12})|(PROCESSO:\d{4}.\d{2}.\d{2}.\d{6}\-\d)|(\d{3,8}\s*.\s *\d{7}.\d{2}.\d{4}.8.23.\d{4})|(\d{3,8}\s*.\d{12}823\d{4})|(\s\d{3,6}\s*.\s*\d{12}\-\d)|(\s+.\s\d{11}.\d)|(\d{4}.\d{2}.\d{6}.\d)|(\d{7}\-\d{2}\.\d{4}\.\d\.?\d{2}\.\d{4})|(\d{3}\.\d{2}\.\d{4}\.\d{6}(\-\d\/\d{6}\-\d{3})?)|(\d{3}\.\d{2}\.\d{6}\-\d))|((Ação\s|Execução)?(Penal:.?.?.?.?|Penal\s?n?..?\s?)(\d{3}\s\d{2}\s\d{6}\s?-?\d|\d{4}.\d{2}.\d?.\d{5}-\d|\d{4}.\d{2}.\d{4}.\d{2}-\d|\s\d{4}.\d{2}.\d{6}-\d|\s\d{12}\s?-\d))')
        expressao_validador = re.compile('(\s?((P|p)enal\s+)|(PENAL\s+)|((C|c)riminal\s+)|(CRIMINAL\s+)|((\sInquerito\s)|(INQUERITO))|((P|p)risão)|(\s+(C|c)rime(s)\s+((C|c)ontra\s+)?)|(\s*Flagrante\s)|((\sHABEAS\s*CORPUS\s)|(\s(H|h)abeas\s)))')
        expressao_cpf = re.compile('(((CPF)(\sn..)?(\s*)?(.{12,16},))|((CPF|cpf|Cpf)|(CPF\/\w{2}\s?sob\s*o\s?))(\s*)?(((N|n)?..\s?)|(\sn..\s))?(\s*)?((\d{11})|(\d{3}..?\d{3}..?\d{3}.?-\d{2})|(\d{3}..?\d{3}.?.\d{5})|(\d{9}-\d{2}))?)')
        expressao_rg = re.compile('((((\sRG(\.{1,3}|\:)?)|(Identidade\s)|(Idently)|(Migratório nº)|(portadora\s*do\s*CGC)|(\sR.?G.?))(\s*)?(((N|n).?.?.?)|(\sRNM\s))?\s*?((.{9,16}\-\d{2})|(\w[A-Z0-9]{6}\-\w)|(.\d*.\d*(.\d)?)|(\d*.\d*)|(\d*).(\d+))(\s*)(\-|)?(\/)?(\s*)?(SSP)?((\/)?(\w{2})|(\s+.\s+\w{2})|(\w{3}\/\w{2})|(\s?(\w+\/\w+)|..?\s+)(\w{3}...?\s?\w{2}))?)|(identidade venezuelana)\s(N|n.{2})\s(.{9}))')
        expressao_rg_valid = re.compile('((\sRG)|(\sIdentidade)|(\s(P|p)ortador\sda\sCI\s)|(\sIdently)|(\sMigratório)|(\sCPF\s?)|(\scpf\s?)|(\sCpf\s?)|(\scnpj\s)|(\sCNPJ\s)|(\sCnpj\s)|(\sidentidade\svenezuelana))')
        expressao_nome = re.compile('((A|a)cusado\(s\):|acusad(a|o)s?:?|INTIMAÇÃO\s+(DE|de)\s?:?|Réu\(s\):?|CITAÇÃO DE:|Réu:|réu\s*|INTIMAD(A|O)|conhecimento,?(\sde)?(\sque):?|(\s*movido\s*em\s*desfavor\s*?de\s*))\s?([A-ZÃÁÂÉÊÍÓÔÕÚÇ\s]+,?\s|[A-Za-zâãáéêíóôõúç\s]+,?\s)')
        expressao_apelido = re.compile('vulgo\s?.([a-zA-ZÂÃÁÉÊÍÔÕÚÇâãáéêíóôõúç\s]+).')
        expressao_nacionalidade = re.compile('(brasileir(a|o))|(venezuelano)')
        expressao_estado_civil = re.compile('solteir.?(a|o)|casad.?(a|o)|divorciad.?(a|o)|viúv.?(a|o)|marital')
        expressao_estado_civil_situacao = re.compile('\(?amasiado\)?|\(?separado\)?')
        expressao_naturalidade = re.compile('natural.de.[a-zA-ZÂÃÁÉÊÍÔÕÚÇâãáéêíóôõúç\s]+((\/\w{2})|(\s?-?\s?\w{2}))?')
        expressao_profissao = re.compile('((ajudante\sde\s?)|(servente\sde\s)|(auxiliar\sde\s?|técnico\sem\s?)?\s+?(cabeleireiro|aposentad(a|o)|operador de máquinas pesadas|autônom(o|a)|desoc.?pado|pensionista|doméstica|serrador|almoxarifado|agricultor|pedreiro|padeiro|pintor|cobrador|garimpeiro|motorista|mecânico|mecânic(o|a)\s?.?(elétrica)?|serviços gerais|lanterneiro|secret.ria|braçal|auxiliar\sadministrativo|administrador(\sde..*empresa)?|estudante|comerciante|comerciário|terraplanagem|marceneiro|eletricista|militar|caseiro|comissária|cabeleireira?|apose|cabeleleira|soldado|zelador(\sde)?|jornalista|vigia|agente\sde\strânsito|funileiro|cozinheiro|taxista|office boy|guarda|manicure|borracheiro|atendente|enfermeiro(\s(ao)?\s?.?doença\s?)?|aposentada|aposentado|babá|baba|cabelereira|motorist(a|e)|vendedor|empregad(o|a)|jardineiro|agente\sprisional|escritório|desempregad(o|a)|sacoleira|pedagoga|pedagogo|banco|dona\sde\scasa|carroceiro|esteticista|administrativa|supervisor|esteticist(a|o)|protesista|operador de empilhadeira|oficial de justiça|agente\sde\strânsito|atendente\sde\sloja|vendedor(a)?\s?.?externo|autônoma|autonomo|caixa\sde\sbanco|juiz\sde\sdireito|líder\sde\sprodução|técnica\sem\ssegurança\sdo\s?trabalho|secretária executiva|zeladora)\s)?')
        expressao_residencia = re.compile('(RUA|AVENIDA|Alameda|Travessa|Estada|Beco|Rodovia|Condomínio|loteamento|Acesso|Quadra|Nº)\s?(.\s?\w+)?\s+?(?:[A-ZÃÁÂÉÊÍÓÔÕÚÇ][a-zãáâéêíóôõúç\s]*){2,}?\s?((Nº\s?\d+)|(\s?(bloco|quadra|lote|apartamento)\s?(.\s?\w+)?\s?((Nº\s?\d+)|(\s\d+\s?[-/]?\s?\d+\s?[-/]?\s?\d+))?)|(\s?\(residencial\)\s?)?)')
        expressao_comarca = re.compile('comarca de\s([A-ZÃÁÂÉÊÍÓÔÕÚÇ][a-zãáâéêíóôõúç\s]*)(\/\w{2})?')
        expressao_sentenca = re.compile('(Decisão\s|Despacho\s|SENTENÇA\s|despachos\sde\s)?(de\s)?(FL\s[0-9]{1,6}\s)|(\s?autos\s(ordinários|extr. ordinário)\sN.\s?[0-9]{1,10}\s?)?((a|A)ssim\s(se\s)?decide)|(FLs\s?[0-9]{1,10}\s[0-9]{1,10})|((e|E)m\srela[cção]{3}(ão|a|ão)\sao(s)?(s)?\sautos|Fl\.[0-9]{1,3}\-[0-9]{1,10}\s+?\d{4}/\d{4}\-[0-9]{2}\.?\d{2}\.?\d{4}|Fl\.[0-9]{1,3}\s+?\d{4}/\d{4}\-[0-9]{2}\.?\d{2}\.?\d{4}|e\spor\sisso\shomologa\sa\s\d+\?\d{4}\/\d{4}\-[0-9]{2}\.?\d{2}\.?\d{4}|resolvo\sjulgar\sinadmissíve[il]|\d{4}.\d{2}.\d{2}.\d{6}\-\d{2}\s?\((em\s.?.?.?\)\se|em\s.?.?.?\))\s?(\d{4}.\d{2}.\d{2}.\d{6}\-\d{2})?(\(em\s.?.?.?\)\se\s)?(em\s.?.?.?\)|de\s[\d\w\s]*em\s[\d\w\s]*)?\s?(haja\s?vista)?(\.?\s?Aguardando\sinforme\sdemais\sfls\.)?|\s+?EM\s?\R(?:F|L)\s+\d{3,6}\s+\d{1,5}.\d{2}\s*\.\s*\d{2}\s*\.\s*\d{4}\s+?\d{2}\s*/\s*\d{4}-\d{2}(\.\d{2})?\.\d{4}\-\d{2}|\s+?EM\s?\R(?:F|L)\s+\d{3,6}\s+\d{1,5}.\d{2}\s*\.\s*\d{2}\s*\.\s*\d{4}\s+?\d{4}\s*/\s*\d{2}|\s+?EM\s?\R(?:F|L)\s+\d{3,6}\s+\d{1,5}.\d{2}\s*\.\s*\d{2}\s*\.\s*\d{4}\s+?\d{4}\s*/\s*\d{2}-\d{2}\.\d{2}\.\d{4}\-\d{2}|\s+?EM\s?\R(?:F|L)\s+\d{3,6}\s+\d{1,5}.\d{2}\s*\.\s*\d{2}\s*\.\s*\d{4}\s+?\d{2}\s*/\s*\d{4}\-\d{2}|\s+?EM\s?\R(?:F|L)\s+\d{3,6}\s+\d{1,5}.\d{2}\s*\.\s*\d{2}\s*\.\s*\d{4}\s+?\d{2}\s*/\s*\d{4}\-\d{2}\.\d{2}\.\d{4}\-\d{2}|\s+?EM\s?\R(?:F|L)\s+\d{3,6}\s+\d{1,5}.\d{2}\s*\.\s*\d{2}\s*\.\s*\d{4}\s+?\d{2}\s*/\s*\d{4}\.\d{2}\.\d{2}\.\d{6}\-\d{2}|\s+?EM\s?\R(?:F|L)\s+\d{3,6}\s+\d{1,5}.\d{2}\s*\.\s*\d{2}\s*\.\s*\d{4}\s+?\d{2}\s*/\s*\d{4}\.\d{2}\.\d{2}\.\d{6}\-\d{2}|\s+?EM\s?\R(?:F|L)\s+\d{3,6}\s+\d{1,5}.\d{2}\s*\.\s*\d{2}\s*\.\s*\d{4}\s+?\d{2}\s*/\s*\d{4}\.\d{2}\.\d{2}\.\d{6}\-\d{2}\s+?\d{4}.\d{2}.\d{2}.\d{6}\-\d{2}|\s+?EM\s?\R(?:F|L)\s+\d{3,6}\s+\d{1,5}.\d{2}\s*\.\s*\d{2}\s*\.\s*\d{4}\s+?\d{2}\s*/\s*\d{4}\.\d{2}.\d{2}.\d{6}\-\d{2}\s+?\d{4}.\d{2}.\d{2}.\d{6}\-\d{2}\s+?\d{4}.\d{2}.\d{2}.\d{6}\-\d{2}\.\d{2}\.\d{2}\.\d{4}\-\d{2}|\s+?EM\s?\R(?:F|L)\s+\d{3,6}\s+\d{1,5}.\d{2}\s*\.\s*\d{2}\s*\.\s*\d{4}\s+?\d{2}\s*/\s*\d{4}\-\d{2}|\s+?EM\s?\R(?:F|L)\s+\d{3,6}\s+\d{1,5}.\d{2}\s*\.\s*\d{2}\s*\.\s*\d{4}\s+?\d{2}\s*/\s*\d{4}-\d{2}(\.\d{2})?\.\d{4}\-\d{2}|\s+?EM\s?\R(?:F|L)\s+\d{3,6}\s+\d{1,5}.\d{2}\s*\.\s*\d{2}\s*\.\s*\d{4}\s+?\d{4}\s*/\s*\d{2}|\s+?EM\s?\R(?:F|L)\s+\d{3,6}\s+\d{1,5}.\d{2}\s*\.\s*\d{2}\s*\.\s*\d{4}\s+?\d{4}\s*/\s*\d{2}-\d{2}\.\d{2}\.\d{4}\-\d{2}|\s+?EM\s?\R(?:F|L)\s+\d{3,6}\s+\d{1,5}.\d{2}\s*\.\s*\d{2}\s*\.\s*\d{4}\s+?\d{2}\s*/\s*\d{4}\-\d{2}\.\d{2}\.\d{4}\-\d{2}|\s+?EM\s?\R(?:F|L)\s+\d{3,6}\s+\d{1,5}.\d{2}\s*\.\s*\d{2}\s*\.\s*\d{4}\s+?\d{2}\s*/\s*\d{4}\.\d{2}\.\d{2}\.\d{6}\-\d{2}|\s+?EM\s?\R(?:F|L)\s+\d{3,6}\s+\d{1,5}.\d{2}\s*\.\s*\d{2}\s*\.\s*\d{4}\s+?\d{2}\s*/\s*\d{4}\.\d{2}\.\d{2}\.\d{6}\-\d{2}\s+?\d{4}.\d{2}.\d{2}.\d{6}\-\d{2}|\s+?EM\s?\R(?:F|L)\s+\d{3,6}\s+\d{1,5}.\d{2}\s*\.\s*\d{2}\s*\.\s*\d{4}\s+?\d{2}\s*/\s*\d{4}\.\d{2}.\d{2}.\d{6}\-\d{2}\s+?\d{4}.\d{2}.\d{2}.\d{6}\-\d{2}\s+?\d{4}.\d{2}.\d{2}.\d{6}\-\d{2}\.\d{2}\.\d{2}\.\d{4}\-\d{2}|\s+?EM\s?\R(?:F|L)\s+\d{3,6}\s+\d{1,5}.\d{2}\s*\.\s*\d{2}\s*\.\s*\d{4}\s+?\d{2}\s*/\s*\d{4}\-\d{2})')
        expressao_advogado = re.compile('advogad(o|a)\s([A-ZÃÁÂÉÊÍÓÔÕÚÇ][a-zãáâéêíóôõúç\s]*\s*){1,4}(\-\s?\w{2})?')
        expressao_oab = re.compile('(\d{4,10}\s?\/?\s?\w{2}\s?)|(\d{4,10}\.\d{2}\s?\/?\s?\w{2})')
        expressao_juiz = re.compile('(MM.??.?.\s)?Juiz\(?a?\)?\sde\sDireito:?\s([A-ZÃÁÂÉÊÍÓÔÕÚÇ][a-zãáâéêíóôõúç\s]*\s*){1,4}')
        expressao_promotor = re.compile('(Dr.?.?.\s)?Promotor\(?a?\)?\sde\sJustiça:?\s([A-ZÃÁÂÉÊÍÓÔÕÚÇ][a-zãáâéêíóôõúç\s]*\s*){1,4}')
        expressao_defensor = re.compile('(Dr.?.?.\s)?Defensor\(?a?\)?\sPúblico:?\s([A-ZÃÁÂÉÊÍÓÔÕÚÇ][a-zãáâéêíóôõúç\s]*\s*){1,4}')
        expressao_testemunha = re.compile('((1ª|2ª|3ª)?\s*testemunha.*?\:?\s*?([A-ZÃÁÂÉÊÍÓÔÕÚÇ][a-zãáâéêíóôõúç\s]*\s*){1,4})')
        expressao_data = re.compile('(\d{2}\/\d{2}\/20\d{2})')
        expressao_assinatura = re.compile('(\s?(\d{2}\/\d{2}\/20\d{2}\s\d{2}\:\d{2})|(\s?[A-ZÃÁÂÉÊÍÓÔÕÚÇ][a-zãáâéêíóôõúç\s]*\s\w{2}\s\d{4})|(\s?[A-ZÃÁÂÉÊÍÓÔÕÚÇ][a-zãáâéêíóôõúç\s]*\s\d{2}\.\d{2}\.\d{4}))')
        lista_processos = []

        for linha in lista_de_linhas:
            if not re.search(nao_pegar, linha):
                processo = {}
                processo['Número do Processo'] = self.tratamento(expressao_npu_numero_proc.search(linha))
                processo['Validador'] = self.tratamento(expressao_validador.search(linha))
                processo['CPF'] = self.tratamento(expressao_cpf.search(linha))
                processo['RG'] = self.tratamento(expressao_rg.search(linha))
                processo['RG Validador'] = self.tratamento(expressao_rg_valid.search(linha))
                processo['Nome'] = self.tratamento(expressao_nome.search(linha))
                processo['Apelido'] = self.tratamento(expressao_apelido.search(linha))
                processo['Nacionalidade'] = self.tratamento(expressao_nacionalidade.search(linha))
                processo['Estado Civil'] = self.tratamento(expressao_estado_civil.search(linha))
                processo['Estado Civil Situação'] = self.tratamento(expressao_estado_civil_situacao.search(linha))
                processo['Naturalidade'] = self.tratamento(expressao_naturalidade.search(linha))
                processo['Profissão'] = self.tratamento(expressao_profissao.search(linha))
                processo['Residência'] = self.tratamento(expressao_residencia.search(linha))
                processo['Comarca'] = self.tratamento(expressao_comarca.search(linha))
                processo['Sentença'] = self.tratamento(expressao_sentenca.search(linha))
                processo['Advogado'] = self.tratamento(expressao_advogado.search(linha))
                processo['OAB'] = self.tratamento(expressao_oab.search(linha))
                processo['Juiz'] = self.tratamento(expressao_juiz.search(linha))
                processo['Promotor'] = self.tratamento(expressao_promotor.search(linha))
                processo['Defensor'] = self.tratamento(expressao_defensor.search(linha))
                processo['Testemunha'] = self.tratamento(expressao_testemunha.search(linha))
                processo['Data'] = self.tratamento(expressao_data.search(linha))
                processo['Assinatura'] = self.tratamento(expressao_assinatura.search(linha))
                lista_processos.append(processo)

        return lista_processos

# Exemplo de uso
arquivo = [
    "VARA CRIMINAL",
    "Processo n. 1234-56.78.9101-1",
    "Réu: João da Silva",
    "Advogado: Dr. José Santos",
    "Sentença: O réu foi condenado",
    "Assinatura: Juiz Fulano de Tal",
    "TRIBUNAL REGIONAL ELEITORAL DE RORAIMA – TRE/RR"
]

extrator = ExtratorProcessoCriminal()
lista_processos = extrator.run(arquivo)

