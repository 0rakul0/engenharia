import re
from functools import reduce
from util.StringUtil import remove_varios_espacos, remove_acentos
import pandas as pd

class ExtratorDJRR():

    def __init__(self):
        self.dict_arquivo = []

    def run(self, arquivo):
        resumo = self.cria_lista_de_linhas(arquivo)
        self.procura_processos_criminal(resumo)

    def tratamento(self, texto):
        if texto:
            texto = texto.group(0)
        else:
            texto = None
        return texto

    def filtro(self, arquivo):
        expressao_padrao = re.compile(
            r'(\d.\sVARA CRIMINAL[\s\S]*?(TRIBUNAL REGIONAL ELEITORAL DE RORAIMA|JUIZADO DA INF.NCIA E JUVENTUDE|PRESID.NCIA))')

        texto = " ".join(arquivo)
        blocos_de_texto = expressao_padrao.findall(texto)

        linhas_isoladas = [bloco[0] for bloco in blocos_de_texto]

        return linhas_isoladas

    def cria_lista_de_linhas_removendo_separador(self,lista_expressoes_ignoradas, separador, arquivo):
        linhas = arquivo  # 0 é o nome do arquivo e 1 é o texto em si
        if linhas != []:

            linhas = list(map(lambda linha: linha + ' SEPARADOR_SEGUNDO_RR ', linhas))
            linhas = ''.join(linhas).split('\n')
            linhas = list(map(lambda linha: remove_acentos(linha), linhas))
            linhas = list(map(lambda linha: re.sub('^\s+', '', linha), linhas))
            linhas = list(filter(lambda linha: linha != '',
                                 list(map(lambda linha: remove_varios_espacos(re.sub('\s*\n', '', linha)), linhas))))
            linhas = list(map(lambda linha: linha + ' SEPARADOR_SEGUNDO_RR ', linhas))

            linhas_concatenadas = ''
            fatia = 10000
            for i in range(0, int(len(linhas) / fatia) + 1):
                if i * fatia < len(linhas):
                    linhas_concatenadas += (remove_acentos(
                        reduce(lambda x, y: x + ' ' + y if not x.endswith('-') else x[:-1] + y,
                               linhas[i * fatia:i * fatia + fatia])))

            for expressao_ignorada in lista_expressoes_ignoradas:
                linhas_concatenadas = expressao_ignorada.sub('', linhas_concatenadas)

            lista_de_linhas = re.split(separador, linhas_concatenadas)
            lista_de_linhas = list(filter(lambda linha: linha != None, lista_de_linhas))[1:]
            lista_de_linhas = list(filter(lambda linha: linha != ' ', lista_de_linhas))
            lista_de_linhas = list(filter(lambda linha: linha != ' (', lista_de_linhas))
            lista_de_linhas = list(map(lambda linha: re.sub('\sSEPARADOR_SEGUNDO_RR\s', ' ', linha), lista_de_linhas))
            lista_de_linhas = list(filter(
                lambda linha: linha != re.search('\A\/\d{2}\s*\(\s*$', linha).group(0) if re.search(
                    '\A\/\d{2}\s*\(\s*$', linha) else ' ', lista_de_linhas))

            regex_npu = re.compile(
                r'(?:PROC\.?(?:ESSO)?\s*(?:N\.\s*:?|\s*N\.)?\s*)?'
                r'(?:\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}|'
                r'\d{3}\.\d{2}\.\d{6}-\d|'
                r'\d{4}\.\d{2}\.\d{2}\.\d{6}-\d|'
                r'\d{8}\.\d/\d.\d{4}-\d{3}|'
                r'(?:\d{4}\.)?\d{13,15}(?:\s+)?\.\d|'
                r'\d{3}\.\d{3}\.\d/\d|'
                r'\d{6,7}\.\d/\d{1,2})'
            )

            for pos, linha in enumerate(lista_de_linhas):
                if re.search(regex_npu, lista_de_linhas[pos]) and re.search(regex_npu, lista_de_linhas[pos + 1]):
                    lista_de_linhas.pop(pos + 1)

            novas_linhas = []

            # For para mesclar a posição i+1 com a posição i, onde i é o texto e i+1 é o npu
            for pos, linha in enumerate(lista_de_linhas):
                if pos % 2 == 0:
                    try:
                        novas_linhas.append(f'{linha} {lista_de_linhas[pos+1]}')
                    except:
                        continue

            return novas_linhas

    def cria_lista_de_linhas(self, arquivo):
        expressao_cabecalho1 = re.compile(
            '(Boa\s*Vista.)?(\s*\d{1,2}\s*de\s*\w*\sde\s\d{4})?(\s*Di.rio\s*da\s*Justiça\s*Eletr.nico\s*)(ANO\s*\w{2,5}\s*.\s*EDI..O\s*\d{2,5}\s*\d{2,4}\/\d{2,4})')
        expressao_cabecalho2 = re.compile(
            '(\s*Di.rio\s*da\s*Justi.a\s*Eletr.nico\s*)(ANO\s*\w{2,4}\s*.\s*EDI..O\s*\d{2,5}\s*\d{2,4}\/\d{2,4})')
        expressao_cabecalho3 = re.compile('((Diário\sdo\sPoder\s(Judiciário|Judicário))\s*((ANO|Ano)\s*\w{2,4}\s*.\s*EDIÇÃO\s*\d{3,5})\s*(Boa\s*Vista\-RR)\,.)')
        expressao_cabecalho4 = re.compile('(Diario\s+do\s+Poder\s+Judiciario\s+ANO\s+.*EDICAO.*Boa\s+Vista\s+\-RR.*\d{2}\sde\s.*de\s\d{4})')
        expressao_cabecalho5 = re.compile('Diario do Poder Judiciario ANO.*EDICAO \d{4} Boa Vista -RR')
        expressao_data = re.compile(" *\d{1,2} *de *[A-Za-zÇç]* *de *20[01]\d")

        lista_expressoes_ignoradas = []
        lista_expressoes_ignoradas.append(expressao_data)
        lista_expressoes_ignoradas.append(expressao_cabecalho1)
        lista_expressoes_ignoradas.append(expressao_cabecalho2)
        lista_expressoes_ignoradas.append(expressao_cabecalho3)
        lista_expressoes_ignoradas.append(expressao_cabecalho4)
        lista_expressoes_ignoradas.append(expressao_cabecalho5)

        """
        separador = re.compile('(^\d{1}..)?((EDITAL\s+?DE\s|Edital\s+de\s)|(PROC.\s*N..\s*)|(\sPUBLICAÇÃO\s*DE\s)|(\sINTIMAÇÃO\s*DE\s*SENTENÇA\s)|(MINISTÉRIO\sPÚBLICO)|(\shttp\:\/\/)|(SECRETARIA\sDA\s)|(\sQUADRO\s*DEMONSTRATIVO\s)|(CRIME\sDE\sTÓXICOS)|(\sJUIZADO\s*DA\s*INFÂNCIA\s)|(\sPRISÃO\s*EM\s*FLAGRANTE\s)|(\sDiretor\s*de\s*Secretaria\s)|(\sTécnica\s*Judiciária\s)|(\sAPELAÇÃO\s*CRIMINAL\s)|((\s?VARA\s(DE\s)?)(CRIMES|CRIMINAL|FEDERAL|CÍVEL|RORAIMA)?)|(PUBLICAÇÃO\s*DE\s*(DECISÃO|DESPACHO|INDENIZAÇÃO|AÇÃO\s*PENAL)\s)|(http:\/\/sei\.tjrr\.jus\.br\/autenticidade)|((Escola|ESCOLA)\s*do\s*(Judiciário\s|JUDICIÁRIO\s))|(\sESCRIVÃ(O)?(\(Ã\)?\:)?)|(\sEscrivã(o)?(\(ã\)?\:)?))|(\s*JUDICIAL|\s*Judicial|\s*SUBSTITUTO)\s|(\sJUSTIÇA\s*DO\s*ESTADO\s)|(\sRELAÇÃO\s*DOS\s*PROCESSOS\s)|(\sTRIBUNAL\s*DE\s*JUSTIÇA\s)|C(OMARCA\sDE\sBOA\sVISTA)|(ÍNDICE\sPOR\sADVOGADOS)|(JUIZADOS\sESPECIAIS)|(\sCONCURSO\s*PÚBLICO\s)|(\sPUBLICAÇÃO\s*PAUTA\s*DOS\s)|(\sCrime\s*C\/\s)|((SICOJURR)?\s*.\s*((\w[a-zA-Z0-9]{12}\/\w[a-zA-Z0-9]{12}=)|(C\+\w[a-zA-Z0-9]{24}=)|(\w[a-zA-Z0-9]{26}=)|(\d{3,8}\s*.\w*[a-zA-Z0-9\/.*\+\-]{26}=)))|(\s\d{3,6}\s*.\s*\d{10,13}\s?\-\s?\d\s)')
        separador = re.compile('(((^\d{1}..)?\s(EDITAL\s*DE\s*|\sPUBLICAÇÃO\s*DE\s*|\sINTIMAÇÃO\s*DE\s*)(NOTIFICAÇÃO|(INTIMAÇÃO|NTIMAÇÃO)|DECISÃO|PRAÇAS|LEILÃO|CONVOCAÇÃO|PROCLAMAS|SENTENÇA|CITAÇÃO))|(E D I TA L D E)|(VARA\s*FEDERAL)|(CIVEL\s*E\s*CRIMINAL)|(CONCURSO|concurso)|(DESIGNAÇÃO\s*DE\s*AUDIÊNCIA)|(\sPUBLICAÇÃO\s*DE\s*ACÓRDÃO\s)|(CITAÇÃO\s)|(\sPUBLICAÇÃO\s*DE\s*SENTENÇA\s)|(PUBLICAÇÃO\s*DE\sDECISÃO)|(\sPROCEDIMENTO\s*ADMINISTRATIVO\s)|(\sESCRIVÃ(O)?\s*JUDICIAL\s)|(\sDIRETORIA\s*GERAL\s)|(\sTRIBUNAL\s*REGIONAL\s*ELEITORAL\s)|(\sCORREGEDORIA\s*GERAL\s*DE\s*JUSTIÇA\s)|(\sMINISTÉRIO\s*PÚBLICO\s*DO\s*ESTADO\s)|(MINISTÉRIO\sPÚBLICO\sPORTARIA)|(Defensoria\sPública\sdo\sEstado\sde\sRoraima)|(\sTERMO\s*DE\s*SORTEIO\s)|((\sTURMA\s*RECURSAL\s*)(EDITAL\s)?)|(JUIZADO\s*DA\s*INFÂNCIA\s*E\s*JUVENTUDE)|(\sJUIZADO\s*ESPECIAL\s)|(Técnica\s*Judiciária\s*-\s*)|(\sDiretor\s*de\s*Secretaria\s)|(Procuradora\sde\sJustiça)|(\sDiretor\-Geral\s)|(\sCâmara\s*\-\s)|(\sInquérito\s*Policial\s)|(\sTécnica\s*Judiciária\s)|(AUTOS\sCOM\s)|(\sCONCURSO\s*PÚBLICO\s)|(\sCOMARCA\sDE\sRORAINÓPOLIS\s)|(\sPUBLICAÇÃO\s*DE\s*DESPACHO\s)|((\sDEFENSORIA\s*PÚBLICA)|(Defensor\sPúblico\-Geral)\s*PORTARIA\s)|(DESPACHO)|(\sPUBLICAÇÃO\s*PAUTA\s*DOS\s)|(\sVARA\s*((CRIMINAL\s)|(DE\s*EXECUÇÃO\s*PENAL)))|(EXECUÇÃO\s*DA\s*PENA\s*DE\s*MULTA)|(\sTRIBUNAL\s*DE\s*JUSTIÇA\s)|(Escrivã\sJudicial)|(SICOJURR)|(ZONA\sELEITORAL\s)|(PUBLIQUE\s?\-\s?SE\.\s*REGISTRE\s?\-\s?SE\.)|(\sEdital\,\s*que\s*será\s*fixado\s*no\s*local\s*de\s*costume\s)|(Faz saber\s*a\s*todos\s*os\s*que\s*o\s*presente\s*Edital)|(Adv\s\-\s)|(Nenhum\sadvogado\scadastrado))')
        """
        separador = re.compile(
            r'\d+[a-zA-Z]*\s*VARA\s*CRIMINAL|CRIME DE T.XICOS|(Autos\:|PROC.*N).*(\d{4}\s\d{2}\s\d{5,6}.*\d|\d{6}\s\d{5}.*\d)|\d{4,5}\s\-\s\d{11}\s\-\s?\d'
        )
        texto_filtrado = self.filtro(arquivo)
        lista_de_linhas = self.cria_lista_de_linhas_removendo_separador(lista_expressoes_ignoradas, separador, texto_filtrado)
        return lista_de_linhas

    def procura_processos_criminal(self, lista_de_linhas):
        """
        função destinada em capturar as informações vindas do txt e salvar como dict

        """
        nao_pegar = re.compile('((Identidade ou Certidão de Nascimento)|(da ))')
        expressao_npu_numero_proc = re.compile('((Processo\sn.\s.{15,16})|(Processo\sn..*\:.{20})|(PROC.\s(N|n).\s.{11,13})|(processo\s*de\s*n.\..{10,12})|(PROCESSO:\d{4}.\d{2}.\d{2}.\d{6}\-\d)|(\d{3,8}\s*.\s *\d{7}.\d{2}.\d{4}.8.23.\d{4})|(\d{3,8}\s*.\d{12}823\d{4})|(\s\d{3,6}\s*.\s*\d{12}\-\d)|(\s+.\s\d{11}.\d)|(\d{4}.\d{2}.\d{6}.\d)|(\d{7}\-\d{2}\.\d{4}\.\d\.?\d{2}\.\d{4})|(\d{3}\.\d{2}\.\d{4}\.\d{6}(\-\d\/\d{6}\-\d{3})?)|(\d{3}\.\d{2}\.\d{6}\-\d))|((Ação\s|Execução)?(Penal:.?.?.?.?|Penal\s?n?..?\s?)(\d{3}\s\d{2}\s\d{6}\s?-?\d|\d{4}.\d{2}.\d?.\d{5}-\d|\d{4}.\d{2}.\d{4}.\d{2}-\d|\s\d{4}.\d{2}.\d{6}-\d|\s\d{12}\s?-\d))')
        expressao_validador = re.compile('(\s?((P|p)enal\s+)|(PENAL\s+)|((C|c)riminal\s+)|(CRIMINAL\s+)|((\sInquerito\s)|(INQUERITO))|((P|p)risão)|(delito)|(\s+(C|c)rime(s)\s+((C|c)ontra\s+)?)|(\s*Flagrante\s)|((\sHABEAS\s*CORPUS\s)|(\s(H|h)abeas\s)))')
        expressao_cpf = re.compile('(((CPF)(\sn..)?(\s*)?(.{12,16},))|((CPF|cpf|Cpf)|(CPF\/\w{2}\s?sob\s*o\s?))(\s*)?(((N|n)?..\s?)|(\sn..\s))?(\s*)?((\d{11})|(\d{3}..?\d{3}..?\d{3}.?-\d{2})|(\d{3}..?\d{3}.?.\d{5})|(\d{9}-\d{2}))?)')
        expressao_rg = re.compile('((((\sRG(\.{1,3}|\:)?)|(Identidade\s)|(Idently)|(Migratório nº)|(portadora\s*do\s*CGC)|(\sR.?G.?))(\s*)?(((N|n).?.?.?)|(\sRNM\s))?\s*?((.{9,16}\-\d{2})|(\w[A-Z0-9]{6}\-\w)|(.\d*.\d*(.\d)?)|(\d*.\d*)|(\d*).(\d+))(\s*)(\-|)?(\/)?(\s*)?(SSP)?((\/)?(\w{2})|(\s+.\s+\w{2})|(\w{3}\/\w{2})|(\s?(\w+\/\w+)|..?\s+)(\w{3}...?\s?\w{2}))?)|(identidade venezuelana)\s(N|n.{2})\s(.{9}))')
        expressao_rg_valid = re.compile('((\sRG)|(\sIdentidade)|(\s(P|p)ortador\sda\sCI\s)|(\sIdently)|(\sMigratório)|(\sCPF\s?)|(\scpf\s?)|(\sCpf\s?)|(\scnpj\s)|(\sCNPJ\s)|(\sCnpj\s)|(\sidentidade\svenezuelana))')
        expressao_nome = re.compile('((A|a)cusado\(s\):|acusad(a|o)s?:?|INTIMAÇÃO\s+(DE|de)\s?:?|Réu\(s\):?|CITAÇÃO DE:|Réu:|réu\s*|INTIMAD(A|O)|conhecimento,?(\sde)?(\sque):?|(\s*movido\s*em\s*desfavor\s*?de\s*))\s?([A-ZÃÁÂÉÊÍÓÔÕÚÇ\s]+,?\s|[A-Za-zâãáéêíóôõúç\s]+,?\s)')
        expressao_apelido = re.compile('vulgo\s?.([a-zA-ZÂÃÁÉÊÍÔÕÚÇâãáéêíóôõúç\s]+).')
        expressao_nacionalidade = re.compile('(brasileir(a|o))|(venezuelano)')
        expressao_estado_civil = re.compile('solteir.?(a|o)|casad.?(a|o)|divorciad.?(a|o)|viúv.?(a|o)|marital')
        expressao_estado_civil_situacao = re.compile('\(?amasiado\)?|\(?separado\)?')
        expressao_naturalidade = re.compile('natural.de.[a-zA-ZÂÃÁÉÊÍÔÕÚÇâãáéêíóôõúç\s]+((\/\w{2})|(\s?-?\s?\w{2}))?')
        expressao_profissao = re.compile('((ajudante\sde\s?)|(servente\sde\s)|(auxiliar\sde\s?|técnico\sem\s?)?\s+?(cabeleireiro|aposentad(a|o)|operador de máquinas pesadas|autônom(o|a)|desoc.?pado|pensionista|doméstica|serrador|almoxarifado|agricultor|pedreiro|padeiro|pintor|cobrador|garimpeiro|motorista|mecânico|mecânic(o|a)\s?.?(elétrica)?|serviços gerais|lanterneiro|secret.ria|braçal|auxiliar\sadministrativo|administrador(\sde..*empresa)?|estudante|comerciante|comerciário|terraplanagem|marceneiro|eletricista|militar|caseir(a|o)|pescador)|eletrônica)')
        expressao_data_de_nascimento = re.compile('((nascido\s*em\s*)|(nascido\s*aos\s*))((\d{2}\/\d{2}\/\d{4})|(\d{2}\.\d{2}\.\d{4})|(\d{2}\-\d{2}\-\d{4}))')
        expressao_filiacao = re.compile('filh(a|o) de [a-zA-ZÂÃÁÉÊÍÔÕÚÇâãáéêíóôõúç\s]+(\se?\s(de)?)?[a-zA-ZÂÃÁÉÊÍÔÕÚÇâãáéêíóôõúç\s]')
        expressao_codigo_penal = re.compile('((artigo\s\d{3}\,\s\§.{2,5}\,)|(\s(ART|art).{1,35}(C.DIGO pena)|(C.DIGO pena).{1,5})|(CP.\s*ART\s*.{3}\:.{4,25}\s?\,)|(art.{2,10},))')

        for id, item in enumerate(lista_de_linhas):
            texto_item = remove_varios_espacos(item)
            processo_validador = self.tratamento(expressao_validador.search(texto_item))
            if processo_validador:
                try:
                    processo_data = f' {dia}/{mes}/{ano}'
                    npu_num_proc = self.tratamento(expressao_npu_numero_proc.search(texto_item))
                    processo_rg = self.tratamento(expressao_rg.search(texto_item))
                    processo_cpf = self.tratamento(expressao_cpf.search(texto_item))
                    processo_nome = self.tratamento(expressao_nome.search(texto_item))
                    processo_apelido = self.tratamento(expressao_apelido.search(texto_item))
                    processo_nacionalidade = self.tratamento(expressao_nacionalidade.search(texto_item))
                    processo_estado_civil = self.tratamento(expressao_estado_civil.search(texto_item))
                    processo_estado_civil_situacao = self.tratamento(expressao_estado_civil_situacao.search(texto_item))
                    processo_naturalidade = self.tratamento(expressao_naturalidade.search(texto_item))
                    processo_profissao = self.tratamento(expressao_profissao.search(texto_item))
                    processo_data_de_nascimento = self.tratamento(expressao_data_de_nascimento.search(texto_item))
                    processo_filiacao = self.tratamento(expressao_filiacao.search(texto_item))
                    processo_estado_civil = processo_estado_civil_situacao if processo_estado_civil_situacao else processo_estado_civil
                    processo_cod_penal = self.tratamento(expressao_codigo_penal.search(item))
                    teor0 = texto_item

                    print(id)
                    print(f'data{processo_data}')
                    print(f'tipo da ação: {processo_validador} --- cod_penal {processo_cod_penal}')
                    print(f'processo: {npu_num_proc}')
                    print(f'rg: {processo_rg} ou cpf: {processo_cpf}')
                    print(f'Nome: {processo_nome}, {processo_apelido}')
                    print(
                        f'nacionalidade: {processo_nacionalidade},'
                        f' naturalidade: {processo_naturalidade},'
                        f' estado civil: {processo_estado_civil},'
                        f' data de nascimento: {processo_data_de_nascimento}')
                    print(f'profissão: {processo_profissao}, {processo_filiacao}')
                    print(teor0)

                    print('\n')

                    dict_processo = {'DATA':processo_data, 'PROCESSO':npu_num_proc,'TIPO DA AÇÃO':processo_validador,
                                     'RG':processo_rg, 'CPF':processo_cpf, 'NOME':processo_nome,
                                     'NACIONALIDADE':processo_nacionalidade, 'NATURALIDADE':processo_naturalidade,
                                     'ESTADO CIVIL':processo_estado_civil, 'PROFISSÃO':processo_profissao,
                                     'FILIAÇÃO':processo_filiacao, 'DATA DE NASCIMENTO':processo_data_de_nascimento,'TEOR':teor0}
                    self.dict_arquivo.append(dict_processo)
                except Exception as e:
                    print(e)


if __name__ == '__main__':
    rr = ExtratorDJRR()

    for ano in range(2003, 2023):
        for mes in range(1, 13):
            if mes < 10:
                mes = "0" + str(mes)
                for dia in range(1, 31):
                    if dia < 10:
                        dia = "0" + str(dia)
                    try:
                        with open(f'../dados/RR/DJRR/txt/{ano}/{mes}/DJRR_{ano}_{mes}_{dia}.txt', encoding='utf-8') as arq:
                            arquivo = arq.readlines()
                            dict_arq = rr.run(arquivo)
                    except Exception as e:
                        print(e)
                        pass

    print(len(rr.dict_arquivo))

    df = pd.DataFrame(rr.dict_arquivo)

    df.to_csv(r'../dados/RR/Roraima.csv', index=True, sep=';')