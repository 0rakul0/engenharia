# -*- coding: utf-8 -*-
import re

import sys

from pdjus.service.MovimentoService import MovimentoService
from pdjus.service.ProcessoService import ProcessoService
from pdjus.dal.ProcessoDao import ProcessoDao
from pdjus.dal.ProcTempDao import ProcTempDao
from pdjus.service.SituacaoProcessoService import SituacaoProcessoService
from util.RegexUtil import RegexUtil
from util.StringUtil import sao_iguais
from util.FalenciaUtil import verifica_texto_decretacao_falencia
from classificadores.ClassificaQuadroCredores import ClassificaQuadroCredores
from classificadores.ClassificaHabilitacaoCredito import ClassificaHabilitacaoCredito
from datetime import datetime
from util.ConfigManager import ConfigManager
from util.EmpresaUtil import procura_empresa_no_movimento

class ClassificaMovimento:
    def __init__(self):
        self.processoService = ProcessoService()
        self.processodao = ProcessoDao()
        self.proctempdao = ProcTempDao()
        self.encontrado = True
        self.situacao_processo_service = SituacaoProcessoService()


    def classifica_movimento_tjsp_falencias(self, movimento, movimento_service):

        regex_util = RegexUtil()
        movimento_service = MovimentoService()

        classificou = False
        mov_id = movimento.id
        mov_texto = movimento.texto
        lista_regex = regex_util.regex_movimento_marcador

        for regex in lista_regex:
            try:
                if mov_texto and mov_texto != '':
                    match_negacao = regex[1].search(mov_texto)

                    if match_negacao is not None and match_negacao.group(0) == '':
                        match_negacao = None

                    if regex[0].search(mov_texto) and not match_negacao:
                        classificou = True
                        movimento_service.seta_movimento_marcador(movimento, regex[2])
                        print(f'Movimento "{mov_id}" foi atribuido ao marcador "{regex[2]}"')

                    if classificou is False and regex[2] == 'decretacao_falencia':
                        if re.search('(DECRET\w*\s*D?[EA]?\s*FALENCIA)|(FALENCIA\s*DECRET\w*)', movimento.tipo_movimento.nome) and not match_negacao:
                            classificou = True
                            movimento_service.seta_movimento_marcador(movimento, regex[2])
                            print(f'Movimento "{mov_id}" foi atribuido ao marcador "{regex[2]}"')

            except Exception as e:
                print(e)

        return classificou

    def classifica_movimentos_tjsp_falencias(self, processo, movimento_service):
        processo = self.processodao.get_por_numero_processo_ou_npu(processo.npu_ou_num_processo)

        if not processo:
            self.encontrado = False
            return
        movimentos = list(processo.movimentos)
        regex_util = RegexUtil()
        movimento_service = MovimentoService()


        for movimento in movimentos:
            classificou = False
            mov_id = movimento.id
            mov_texto = movimento.texto
            lista_regex = regex_util.regex_movimento_marcador

            for regex in lista_regex:
                try:
                    if mov_texto and mov_texto != '':
                        match_negacao = regex[1].search(mov_texto)

                        if match_negacao is not None and match_negacao.group(0) == '':
                            match_negacao = None

                        if regex[0].search(mov_texto) and not match_negacao:
                            classificou = True
                            movimento_service.seta_movimento_marcador(movimento, regex[2])
                            print(f'Movimento "{mov_id}" foi atribuido ao marcador "{regex[2]}"')

                        if classificou is False and regex[2] == 'decretacao_falencia':
                            if re.search('(DECRET\w*\s*D?[EA]?\s*FALENCIA)|(FALENCIA\s*DECRET\w*)', movimento.tipo_movimento.nome) and not match_negacao:
                                classificou = True
                                movimento_service.seta_movimento_marcador(movimento, regex[2])
                                print(f'Movimento "{mov_id}" foi atribuido ao marcador "{regex[2]}"')

                except Exception as e:
                    print(e)


    def classifica(self,movimento,acompanhamento=''):
        # if movimento.processo.is_processo_falencia_recuperacao_convolacao():
        #     self.verifica_quadro_credores(movimento)
        if movimento.processo.is_processo_da_classe_ou_assunto('habilitacao') and movimento.processo.is_processo_da_classe_ou_assunto('credito'):
            self.verifica_habilitacao_credito(movimento)
        if movimento.processo.is_processo_falencia_recuperacao_convolacao() or (movimento.processo.is_processo_da_classe_ou_assunto('habilitacao') and movimento.processo.is_processo_da_classe_ou_assunto('credito')):
            procura_empresa_no_movimento(movimento,acompanhamento)
        # self.valida_movimento_de_falencia(movimento)
        # self.valida_movimento_de_recuperacao(movimento)
        # self.valida_movimento_esaj(movimento)

    def verifica_habilitacao_credito(self,movimento):
        if not movimento.texto or movimento.texto == '':
            return
        classificaHabCred = ClassificaHabilitacaoCredito('Falencias')
        classificaHabCred.verifica_habilitacao_credito(movimento)

    # só o quadro do movimento chama esse método
    def verifica_quadro_credores(self,movimento,fonte_dado='MOVIMENTO - SAJ',debug=True):
        verQuadro = ClassificaQuadroCredores('Falencias')
        if verQuadro.verifica_possibilidade_de_quadro(movimento.texto):
            verQuadro.verifica_quadro_credores(movimento.texto, movimento.data, movimento.processo, fonte_dado=fonte_dado,movimento=movimento,debug=debug)


    def verifica_indeferido_recuperacao_judicial_em_movimento(self,texto):
        return "INDEFERIDO" in texto and (sao_iguais(texto,"INDEFERIDO O PEDIDO DE RECUPERACAO DE FALENCIA")\
                    or sao_iguais(texto,"INDEFIRO O PEDIDO DE RECUPERACAO JUDICIAL")\
                    or sao_iguais(texto,"INDEFIRO O PEDIDO DE RECUPERACAO EXTRAJUDICIAL")\
                    or sao_iguais(texto,"INDEFIRO O PLANO DE RECUPERACAO EXTRAJUDICIAL")\
                    or sao_iguais(texto,"INDEFIRO O PLANO DE RECUPERACAO JUDICIAL")\
                    or sao_iguais(texto,"INDEFIRO O PLANO DE RECUPERACAO DE FALENCIA") or re.search("INDEFIRO *O *PEDIDO *DA[S]? *RECUPERANDA",texto))

    def verifica_deferido_recuperacao_judicial_em_movimento(self,texto):
        return "DEFERIDO" in texto and (sao_iguais(texto,"DEFERIDO O PEDIDO DE RECUPERACAO DE FALENCIA")\
                    or sao_iguais(texto,"DEFERIDO O PEDIDO DE RECUPERACAO JUDICIAL")\
                    or sao_iguais(texto,"DEFERIDO O PEDIDO DE RECUPERACAO EXTRAJUDICIAL") or re.search("DEF((IRO)|(ERID[OA])) *[OA] *(PROCESSAMENTO)? *(DA)? *RECUPERACAO *(JUDICIAL)?",texto))

    def verifica_homologado_recuperacao_judicial_em_movimento(self,texto):
        return "HOMOLOG" in texto and (sao_iguais(texto,"HOMOLOGADO PLANO DE RECUPERACAO JUDICIAL")\
                    or sao_iguais(texto,"HOMOLOGADO PLANO DE RECUPERACAO EXTRAJUDICIAL")\
                    or sao_iguais(texto,"HOMOLOGADO PLANO DE RECUPERACAO DE FALENCIA") or re.search("HOMOLOG(O|(AD[AO])) *[OA]? *PLANO *(DE)? *RECUPERACAO",texto))

    def verifica_encerramento_recuperacao_judicial_em_movimento(self,texto):
        return "ENCERRA" in texto and (sao_iguais(texto,"ENCERRADA RECUPERACAO JUDICIAL")\
                    or sao_iguais(texto,"ENCERRADA RECUPERACAO EXTRAJUDICIAL")\
                    or sao_iguais(texto,"ENCERRADA RECUPERACAO DE FALENCIA") or re.search("((DECRET(O|(ADO)) *O *ENCERRAMENTO)|ENCERRO) *(D)?A *RECUPERACAO",texto))

    # Falta generalizar
    def valida_movimento_de_recuperacao(self,movimento):
        if not movimento.tipo_movimento or not movimento.processo.is_processo_falencia_recuperacao_convolacao():
            return
        texto_tipo = ""
        texto_movimento = ""
        if movimento.tipo_movimento:
            texto_tipo = movimento.tipo_movimento.nome
        if movimento.texto:
            texto_movimento = movimento.texto

        # Para nao dar problema com o sao iguais:
        # PEDIDOS INDEFERIDOS
        if self.verifica_indeferido_recuperacao_judicial_em_movimento(texto_tipo) or self.verifica_indeferido_recuperacao_judicial_em_movimento(texto_movimento):
            
            self.situacao_processo_service.preenche_situacao_processo(movimento.processo, "INDEFERIDO",movimento.data)

        # PEDIDOS DEFERIDOS
        if self.verifica_deferido_recuperacao_judicial_em_movimento(texto_tipo) or self.verifica_deferido_recuperacao_judicial_em_movimento(texto_movimento):

            self.situacao_processo_service.preenche_situacao_processo(movimento.processo, "DEFERIDO",
                                                                        movimento.data)

        # PLANOS HOMOLOGADOS
        elif self.verifica_homologado_recuperacao_judicial_em_movimento(texto_tipo) or self.verifica_homologado_recuperacao_judicial_em_movimento(texto_movimento):
                
            self.situacao_processo_service.preenche_situacao_processo(movimento.processo, "HOMOLOGADO PLANO",
                                                                            movimento.data)

        # RECUPERAÇÕES ENCERRADAS
        elif self.verifica_encerramento_recuperacao_judicial_em_movimento(texto_tipo) or self.verifica_encerramento_recuperacao_judicial_em_movimento(texto_movimento):
            
            self.situacao_processo_service.preenche_situacao_processo(movimento.processo, "ENCERRADO",
                                                                            movimento.data)

        self.processoService.salvar(movimento.processo)

    def verifica_decretacao_falencia_em_movimento(self,texto):
        if not texto:
            return False
        return re.search("DEC((RETO)|LARO) A(BERTA *A?)? ((FALENCIA)|(QUEBRA))",texto)  \
               # or re.search("DEC((RETO)|LARO) A(BERTA A)? QUEBRA",texto)

            # sao_iguais(texto,"DECRETADA FALENCIA") \
               # or sao_iguais(texto,"DECRETADA A FALENCIA") \

    # or texto == "SENTENCA PROCEDENTE" \

    def verifica_encerramento_falencia_em_movimento(self,texto):
        if not texto:
            return False
        return sao_iguais(texto,"FALENCIA ENCERRADA") or re.search("EDITAL *-?(DE)? *ENCERRAMENTO *D[AE] *FAL.NCIA",texto)



    def valida_movimento_de_falencia(self,movimento):
        if not movimento.tipo_movimento or not movimento.processo.is_processo_falencia_recuperacao_convolacao():
            return
        if self.verifica_decretacao_falencia_em_movimento(movimento.tipo_movimento.nome) or self.verifica_decretacao_falencia_em_movimento(movimento.texto):
            self.situacao_processo_service.preenche_situacao_processo(movimento.processo, "DECRETADO",
                                                                      movimento.data)

        if self.verifica_encerramento_falencia_em_movimento(movimento.tipo_movimento.nome) or self.verifica_encerramento_falencia_em_movimento(movimento.texto):
            self.situacao_processo_service.preenche_situacao_processo(movimento.processo, "ENCERRADO",
                                                                      movimento.data)
        if sao_iguais(movimento.tipo_movimento.nome,"SENTENCA ANULADA"):
            self.situacao_processo_service.preenche_situacao_processo(movimento.processo, "ANULADO",
                                                                      movimento.data)
        self.processoService.salvar(movimento.processo)

    def valida_movimento_esaj(self,movimento):
        if not movimento.tipo_movimento or not movimento.processo.is_processo_falencia_recuperacao_convolacao():
            return
        if(sao_iguais(movimento.tipo_movimento.nome, 'PROCESSO EXTINTO')):
            self.situacao_processo_service.preenche_situacao_processo(movimento.processo, "EXTINTO",
                                                                      movimento.data)
        else:
            #P é o num processo que é retornado caso encontrado no texto, nesse caso não usamos.
            encontrou,p = verifica_texto_decretacao_falencia(movimento.texto)
            if encontrou:
                if not movimento.processo.contains_situacao('DECRETADO'):
                    self.situacao_processo_service.preenche_situacao_processo(movimento.processo, "DECRETADO",
                                                                              movimento.data)
        self.processoService.salvar(movimento.processo)

# DESCOMENTAR PARA TESTAR REGEX DO QUADRO
if __name__ == '__main__':

    c = ClassificaMovimento()
    rank = 2
    fatia = 3
    # processos = c.processodao.get_processo_filtra_tag_data_atualizacao(tag='FALENCIAS', dias=240, distinct=True)
    # processos = list(filter(lambda x: x.id == 16407, processos))
    #processos = list(set(processos))
    processos = c.proctempdao.listar_nao_processados(tag='FALENCIAS', rank=rank, fatia=fatia, limit=1000)
    #processos = list(filter(lambda x: x.numero == '00490645320128260100', processos))

    while len(processos) > 0:

        for id, processo in enumerate(processos, 1):
            processo.processado = True
            print(f'[ {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} ] - {id}/{len(processos)} - Verificando movimentos do processo: {processo.numero}')
            c.classifica_movimentos_tjsp_falencias(processo)
            processo.encontrado = c.encontrado
            c.proctempdao.salvar(processo)
            c.encontrado = True

        processos = c.proctempdao.listar_nao_processados(tag='FALENCIAS', rank=rank, fatia=fatia, limit=1000)

    #movimento_service = MovimentoService()
    # movs = list(set(movimento_service.dao.listar_possiveis_quadro_credores(rank=sys.argv[1], fatia=sys.argv[2])))
    # lista = [
    #     '10773083820138260100',
    #     '00041338220148260491',
    #     '00132759120088260048',
    #     '01465583020038260100',
    #     '00381535020098260564',
    #     '634420038260576',
    #     '00006956820088260035',
    #     '27420098260415',
    #     '00007992520088260079',
    #     '00001140320098260299',
    #     '00002677320098260028',
    #     '00003371120098260022',
    #     '00001073620108260538',
    #     '00006560220098260176',
    #     '10099939520158260302',
    #     '00003684620108260038',
    #     '00007019620108260361',
    #     '40262774120138260224',
    #     '00015382020108260146',
    #     '00012138820088260025',
    #     '00014905020058260659',
    #     '10031381920148260114',
    #     '00010209820108260673',
    #     '00016354420058260615',
    #     '00022167820088260025',
    #     '00019561720108260482',
    #     '00028915220058260120',
    #     '00029671920088260493',
    #     '00021165820108260315',
    #     '77820028260565',
    #     '00040510920088260185',
    #     '00038548820008260038',
    #     '00043432420088260272',
    #     '00023778920048260070',
    #     '00047281520008260510',
    #     '00003902120018260588',
    #     '00033084620108260082',
    #     '00054533820088260408',
    #     '00035215620038260451',
    #     '00057005520088260299',
    #     '00038149620038260363',
    #     '00047549420058260297',
    #     '00039671420038260272',
    #     '10000238920118260115',
    #     '00050814220058260296',
    #     '10152878820148260068',
    #     '00051076620108260554',
    #     '00060208320058260405',
    #     '00009701420098260348',
    #     '00046742720048260278',
    #     '00047236920048260019',
    #     '00014454520018260252',
    #     '00049391920048260637',
    #     '00072205320058260526',
    #     '00114140620008260451',
    #     '00047398620098260394',
    #     '00084270620058260650',
    #     '00086076420058260248',
    #     '00021745320098260038',
    #     '00497645020098260224',
    #     '00180793820008260451',
    #     '00026042720098260451',
    #     '00111895520058260533',
    #     '00058495220108260082',
    #     '00118385820058260100',
    #     '00062633620088260562',
    #     '00064328920088260152',
    #     '00075789520038260038',
    #     '00125509420058260602',
    #     '05048174720008260100',
    #     '174320128260575',
    #     '00069312520088260362',
    #     '6.96539E+16',
    #     '00039911820098260309',
    #     '00076689520038260655',
    #     '10117601220158260451',
    #     '05172793620008260100',
    #     '00021605820028260606',
    #     '284520128260390',
    #     '738720128260248',
    #     '00121309820038260363',
    #     '05360177220008260100',
    #     '00024373320028260361',
    #     '00043769120098260526',
    #     '00163439120058260068',
    #     '01526127020078260100',
    #     '00076361420108260019',
    #     '00077461920088260363',
    #     '00045426720098260286',
    #     '00170320520058260176',
    #     '05657958720008260100',
    #     '00178750320058260068',
    #     '00185776120058260451',
    #     '00187601720058260068',
    #     '00051959120098260602',
    #     '3.21602E+16',
    #     '05931090820008260100',
    #     '00109727820038260566',
    #     '00001568420138260146',
    #     '00096398920088260510',
    #     '00220937420058260068',
    #     '00031147220028260358',
    #     '06185777120008260100',
    #     '00233304620058260068',
    #     '10009961820158260337',
    #     '00096945020088260248',
    #     '00009187920068260588',
    #     '00077105320108260024',
    #     '00003360320138260146',
    #     '00079067820108260038',
    #     '00037097720028260453',
    #     '06310309820008260100',
    #     '00015334120068260177',
    #     '00114617820088260554',
    #     '00016512420068260498',
    #     '00018625520068260435',
    #     '00061498320018260161',
    #     '00019649420068260106',
    #     '00680908120058260100',
    #     '00097836020108260068',
    #     '00072550320018260510',
    #     '00078037920098260176',
    #     '00122780520088260438',
    #     '00081429120098260320',
    #     '00027327320068260347',
    #     '00132562520088260068',
    #     '00106342720108260286',
    #     '00364586720048260554',
    #     '00145413020038260100',
    #     '00134808620088260609',
    #     '00110684420108260309',
    #     '00086217620098260161',
    #     '00139547020088260152',
    #     '00051442520128260457',
    #     '00114382020108260019',
    #     '00132836720018260451',
    #     '10049340820158260309',
    #     '00111634720128260457',
    #     '00045483220028260347',
    #     '00117059320108260438',
    #     '00039233120068260323',
    #     '00146580920088260597',
    #     '00027142320148260654',
    #     '10085599320148260597',
    #     '00130887120108260482',
    #     '00042460920068260526',
    #     '00009412120128260101',
    #     '00209141820038260152',
    #     '00226047120038260576',
    #     '001416587200982604380',
    #     '00671983320058260114',
    #     '00110405420098260554',
    #     '00151620320088260019',
    #     '10024255820148260271',
    #     '00156171220088260554',
    #     '00128782020098260073',
    #     '00136720920098260019',
    #     '00138611620098260268',
    #     '00207659520088260362',
    #     '00334034920038260100',
    #     '10007121920158260431',
    #     '00001105020138260161',
    #     '00065623020068260191',
    #     '00055835320148260655',
    #     '10132798820148260602',
    #     '00070112920068260048',
    #     '00015280520128260146',
    #     '00002263220138260363',
    #     '00072595220068260320',
    #     '00145474820108260114',
    #     '00146856020108260196',
    #     '00241009020088260114',
    #     '00246425620088260196',
    #     '00159694120108260152',
    #     '00033927920128260663',
    #     '00807115220018260100',
    #     '00260595720088260224',
    #     '00268659420088260482',
    #     '00083491720028260068',
    #     '00075806720068260068',
    #     '00700799320038260100',
    #     '00723377620038260100',
    #     '01138032120018260100',
    #     '01745080920018260577',
    #     '00969055920038260100',
    #     '00207341320108260554',
    #     '00190747920098260566',
    #     '00334929520088260068',
    #     '00190756420098260566',
    #     '00212002720108260224',
    #     '01315077620038260100',
    #     '03363134420018260100',
    #     '00234033620108260361',
    #     '00396875220088260309',
    #     '00031073720128260453',
    #     '00006015220118260347',
    #     '00026015420118260596',
    #     '10007811120158260218',
    #     '01950467420028260577',
    #     '00246011820108260100',
    #     '00109960420028260482',
    #     '00144605220118260019',
    #     '00036133620118260586',
    #     '00105182520128260068',
    #     '00482295320088260602',
    #     '00145898220098260292',
    #     '00521677920088260562',
    #     '00521686420088260562',
    #     '00045301020128260137',
    #     '00123155220118260268',
    #     '00204139020068260562',
    #     '00006013520118260094',
    #     '3.39812E+15',
    #     '09025423520128260037',
    #     '00151133120098260114',
    #     '00642222020088260576',
    #     '00162520720028260100',
    #     '07183757319988260100',
    #     '00161820520098260048',
    #     '00064389120078260068',
    #     '00328248420108260576',
    #     '00041593120118260606',
    #     '00171982020128260361',
    #     '01098922520068260100',
    #     '00064418120118260108',
    #     '00097543820118260597',
    #     '00723609620078260224',
    #     '00216279120098260019',
    #     '1.48676E+16',
    #     '10006276820158260581',
    #     '00221049220098260576',
    #     '00025538120078260161',
    #     '00025712320078260252',
    #     '00223510420098260114',
    #     '00230469320098260554',
    #     '30001514920138260586',
    #     '00028775620078260360',
    #     '00100632320128260048',
    #     '00010027320128260296',
    #     '00273573320098260068',
    #     '00218638120078260320',
    #     '00041710820078260114',
    #     '00284089820098260482',
    #     '00295619420098260506',
    #     '10016885820138260152',
    #     '00298388520098260482',
    #     '01207767920078260100',
    #     '02189725020088260100',
    #     '00010928620128260068',
    #     '30010011920128260108',
    #     '11080622620148260100',
    #     '00364155720098260554',
    #     '00377368620098260309',
    #     '1.48591E+16',
    #     '03823631120088260577',
    #     '07236083219908260100',
    #     '00064825220128260451',
    #     '01381351820028260100',
    #     '00051081220078260019',
    #     '00048370420148260586',
    #     '00025639620128260114',
    #     '10318273420148260224',
    #     '10791938720138260100',
    #     '00027244720128260457',
    #     '00027532320128260320',
    #     '00034275120128260271',
    #     '00696772920098260576',
    #     '00523534320028260100',
    #     '00077929620078260248',
    #     '40022106920138260302',
    #     '40001159120138260132',
    #     '01046961620028260100',
    #     '10370660320148260100',
    #     '00024256620118260114',
    #     '00044678120128260299',
    #     '00030415120118260337',
    #     '00216751020128260451',
    #     '01246911520028260100',
    #     '00347791320128260405',
    #     '03405824320078260577',
    #     '00029187120138260082',
    #     '00111547920078260451',
    #     '00117286820078260624',
    #     '00240818720118260079',
    #     '00039465020118260242',
    #     '00030674520138260348',
    #     '00139897220078260602',
    #     '00571221120138260100',
    #     '00049394820138260299',
    #     '00053629220128260347',
    #     '00521280820108260564',
    #     '30006873820138260076',
    #     '00035620820138260472',
    #     '00058730420128260505',
    #     '00063250420118260358',
    #     '00302410620078260068',
    #     '00066599820128260068',
    #     '10003029620168260698',
    #     '00069452620128260408',
    #     '00579709520138260100',
    #     '00434328020118260100',
    #     '00075833820128260609',
    #     '00073909120118260048',
    #     '00578399120118260100',
    #     '00079163120118260348',
    #     '00079413120118260320',
    #     '00513081320118260577',
    #     '00249677820078260224',
    #     '00088360420118260510',
    #     '00091324820118260438',
    #     '00332322520118260161',
    #     '00252076520078260451',
    #     '00270861020078260451',
    #     '10097999520158260302',
    #     '10034546620148260038',
    #     '00041696620138260554',
    #     '00030541520158260368',
    #     '00103194220128260152',
    #     '00316138420078260554',
    #     '00717220620098260576',
    #     '01275246920038260100',
    #     '00351208020128260068',
    #     '10481474620148260100',
    #     '00049121220148260176',
    #     '10086596420158260451',
    #     '00046379720138260564',
    #     '00141171420128260248',
    #     '06018584320028260100',
    #     '11296401120158260100',
    #     '10012888820098260506',
    #     '30045692220128260309',
    #     '00141480520118260269',
    #     '00157744320118260048',
    #     '11062663420138260100',
    #     '10859734320138260100',
    #     '00171531520118260114',
    #     '00255350520128260100',
    #     '10760092620138260100',
    #     '00191278420118260309',
    #     '00199000920128260564',
    #     '00196716920118260019',
    #     '00200044120128260292',
    #     '40006207120138260362',
    #     '10371333120158260100',
    #     '00599463220128260114',
    #     '00204274420128260019',
    #     '00285095220118260196',
    #     '10052096120158260533',
    #     '10253872220148260224',
    #     '11155260420148260100',
    #     '10028372320158260604',
    #     '00461697220118260224',
    #     '10023010720158260347',
    #     '10878415620138260100',
    #     '11166814220148260100',
    #     '10005442520148260278',
    #     '10051747420158260445',
    #     '00660711120118260224',
    #     '10488694620158260100',
    #     '685419838260451',
    #     '10202812920158260100',
    #     '10837643320158260100',
    #     '10144771720148260100',
    #     '40058704720138260019',
    #     '00005475520148260291',
    #     '10044785920148260320',
    #     '10021392520158260278',
    #     '00565270420128260114',
    #     '00045031420148260539',
    #     '10028516420158260100',
    #     '10052756420148260278',
    #     '10750228720138260100',
    #     '10692008320148260100',
    #     '10011306220158260299',
    #     '00088912820068260510',
    #     '00034833320158260157',
    #     '10971962220158260100',
    #     '00090529020068260428',
    #     '00266000420138260196',
    #     '00094888520068260319',
    #     '00108741120068260624',
    #     '10120146220148260566',
    #     '10803639420138260100',
    #     '10109220720158260019',
    #     '10011994620148260100',
    #     '00196818920068260019',
    #     '10028443920168260132',
    #     '00210868320068260562',
    #     '00383283920138260100',
    #     '10029090820158260637',
    #     '10079897520168260100',
    #     '10198468220158260576',
    #     '40272656220138260224',
    #     '10720530220138260100',
    #     '10087572120148260019',
    #     '10221881120158260562',
    #     '10031188420158260278',
    #     '10027551920138260068',
    #     '10013801120168260348',
    #     '10050089220148260278',
    #     '3.06704E+16',
    #     '10940252820138260100',
    #     '10173772820148260114',
    #     '40093710320138260506',
    #     '10887477520158260100',
    #     '10150714920158260309',
    #     '10006512720138260271',
    #     '10090678920148260451',
    #     '11282149520148260100',
    #     '40082354120138260224',
    #     '11170301120158260100',
    #     '40000882920138260320',
    #     '10011875020148260482',
    #     '10154818920148260100',
    #     '10042427820158260577',
    #     '10125219220168260100',
    #     '10683733820158260100',
    #     '11023156120158260100',
    #     '11315628720158260100',
    #     '00390662720138260100',
    #     '08204491619958260100',
    #     '05043025119968260100',
    #     '40065727420138260477',
    #     '10347992420158260100',
    #     '11324730220158260100',
    #     '00467433619988260100',
    #     '00203491719838260100',
    #     '00511309419988260100',
    #     '10041384920138260127',
    #     '10096707020148260320',
    #     '10834083820158260100',
    #     '10258241320158260100',
    #     '09322887519978260100',
    #     '10008399520158260482',
    #     '10076574120158260554',
    #     '11145306920158260100',
    #     '10368310220158260100',
    #     '10270516220158260577',
    #     '10471448520168260100',
    #     '10760190220158260100',
    #     '10018614120168260358',
    #     '10052455420168260344',
    #     '07121365319988260100',
    #     '10543660720168260100',
    #     '10011228119968260451',
    #     '07414062519988260100',
    #     '40039582920138260079',
    #     '11303930220148260100',
    #     '10240140320158260100',
    #     '09175366419988260100',
    #     '08005334019888260100',
    #     '10678875320158260100',
    #     '10014977820158260431',
    #     '09000733719838260100',
    #     '00263928020068260320',
    #     '00021687120038260615',
    #     '00030682620158260650',
    #     '00112053720038260320',
    #     '00143616220138260100',
    #     '10161031720148260506',
    #     '00287134020048260100',
    #     '00354628720108260577',
    #     '00272565020118260577',
    #     '00384393820038260564',
    #     '01490005620098260100',
    #     '09099134619988260100',
    #     '10001670820168260400',
    #     '10009264220138260152',
    #     '10009601420148260271',
    #     '10009882720158260471',
    #     '10010347120168260506',
    #     '10021916820168260348',
    #     '10022230620168260338',
    #     '10022656220168260659',
    #     '10040458320168260482',
    #     '10056162220158260451',
    #     '10071457720168260019',
    #     '10101414220168260506',
    #     '10131620920148260114',
    #     '10204689220158260114',
    #     '10271596320158260554',
    #     '10274520320168260100',
    #     '10277969720168260224',
    #     '10548891920168260100',
    #     '10560965320168260100',
    #     '10628475620168260100',
    #     '00022932020028260180',
    #     '00011759520038260431',
    #     '08202543119958260100',
    #     '07114826619988260100',
    #     '08308751420008260100',
    #     '01532126720028260100',
    #     '01385246620038260100',
    #     '00727522520048260100',
    #     '05255157420008260100',
    #     '05259548520008260100',
    #     '05753469120008260100',
    #     '01180747320018260100',
    #     '03050413220018260100',
    #     '01684148420028260100',
    #     '00745981420038260100',
    #     '01384050820038260100',
    #     '01592229320038260100',
    #     '00588223720048260100',
    #     '01258979320048260100',
    #     '08327504320058260100',
    #     '08327521320058260100',
    #     '00326589820058260100',
    #     '00363198520058260100',
    #     '05086715919948260100',
    #     '05188640219958260100',
    #     '01500707920078260100',
    #     '03245973920098260100',
    #     '00007806720108260008',
    #     '00122285220108260100',
    #     '00345211620108260100',
    #     '07011406320128260695',
    #     '30045927520138260650',
    #     '10075020620148260576',
    #     '10017695720148260609',
    #     '10023155020148260565',
    #     '10210147220148260506',
    #     '00047009320148260045',
    #     '10219225220148260564',
    #     '10228710920148260554',
    #     '10269301620148260562',
    #     '10092812820158260554',
    #     '10113763120158260554',
    #     '30009335020138260297',
    #     '10158192520158260554',
    #     '10078042720148260223',
    #     '10262308020158260602',
    #     '00025118520148260452',
    #     '10028758920158260586',
    #     '10249849620158260554',
    #     '10250411720158260554',
    #     '10005596920168260586',
    #     '10052175920148260408',
    #     '00025967020158260150',
    #     '10689545320158260100',
    #     '10065986020158260152',
    #     '00027666920158260238',
    #     '10430374820158260224',
    #     '10044188120158260278',
    #     '10016904020168260114',
    #     '00033120820158260115',
    #     '10231121220168260554',
    #     '00034483520158260396',
    #     '10245391420168260564',
    #     '10041595920168260114',
    #     '10001169620168260076',
    #     '10037422720158260281',
    #     '10197324020168260114',
    #     '10009291620158260511',
    #     '10007438020168260309',
    #     '10014334720168260362',
    #     '10274435720168260224',
    #     '10012671220168260363',
    #     '10008676820168260372',
    #     '10606728920168260100',
    #     '10035137720168260428',
    #     '10030115220168260101',
    #     '10130310320168260037',
    #     '10777300820168260100',
    #     '00359607620108260451',
    #     '10309102820168260100',
    #     '00291569720058260506',
    #     '03454904620078260577',
    #     '00069891320148260299',
    #     '01092490420058260100',
    #     '10027071720168260404',
    #     '10206288020168260309',
    #     '01982209120078260100',
    #     '10042118320168260428',
    #     '00030198220138260220',
    #     '10037458420168260462',
    #     '00001215120058260358',
    #     '01073694520038260100',
    #     '10391874920168260224',
    #     '10067586120168260278',
    #     '00020706220158260584',
    #     '00020697720158260584',
    #     '00027361220138260268',
    #     '10003744020158260562',
    #     '00102532120148260337',
    #     '10993403220168260100',
    #     '10143885620168260477',
    #     '10162259020168260625',
    #     '10935714320168260100',
    #     '00065206020058260079',
    #     '02158356020038260577',
    #     '00012457420158260534',
    #     '10005816820158260035',
    #     '10201503420168260451',
    #     '11313668320168260100',
    #     '10034786320058260506',
    #     '10049342120168260358',
    #     '10034769320058260506',
    #     '10036436220168260462',
    #     '03738660820088260577',
    #     '00003966820168260146',
    #     '10143856620148260576',
    #     '00012454820158260187',
    #     '00103517720038260438',
    #     '10128911520168260248',
    #     '10164223420178260100',
    #     '01159654720058260100',
    #     '00800795520038260100',
    #     '05570805620008260100',
    #     '00013233020018260576',
    #     '00010010220038260653',
    #     '10008567620178260510',
    #     '10016200420178260400',
    #     '10023746620178260554',
    #     '10004613320178260624',
    #     '10428419120178260100',
    #     '10244329420178260576',
    #     '10060875220178260068',
    #     '10028046820178260602',
    #     '10128621420178260576',
    #     '10439253020178260100',
    #     '10069156320178260451',
    #     '10145672020178260100',
    #     '10018437620178260619',
    #     '10004029020178260027',
    #     '10023887820178260189',
    #     '10007907220178260615',
    #     '10219654520178260576',
    #     '10472354420178260100',
    #     '10123483020178260554',
    #     '002333046200582600681',
    #     '002333046200582600682',
    #     '10079095320178260302',
    #     '10069341820178260565',
    #     '10023519520178260045',
    #     '10007582720178260111',
    #     '10075896520178260152',
    #     '10121249520178260068',
    #     '10053121020178260271',
    #     '10080729520178260152',
    #     '10740273520178260100',
    #     '10699049120178260100',
    #     '10724692820178260100',
    #     '11307383120158260100',
    #     '10906091320178260100',
    #     '10916034120178260100',
    #     '11012912720178260100',
    #     '11077037120178260100',
    #     '10014096020178260337',
    #     '00044211920128260291',
    #     '10018397320158260695',
    #     '10008169720178260315',
    #     '10124090620178260451',
    #     '10162649420178260482',
    #     '10042747420178260428',
    #     '00162887620078260196',
    #     '11173603720178260100',
    #     '10082509320178260362',
    #     '10054785620178260428',
    #     '10056301320178260038',
    #     '10075621020188260100',
    #     '10000183720178260542',
    #     '10213131720178260224',
    #     '10019874220178260654',
    #     '10320967620178260577',
    #     '10011634320178260538',
    #     '10077328820168260152',
    #     '10201063020188260100',
    #     '10010960420178260595',
    #     '10929553920148260100',
    #     '11081618820178260100',
    #     '00421381720168260100',
    #     '10653291120158260100',
    #     '10048481420178260100',
    #     '00880076620178260100',
    #     '11327810420168260100',
    #     '10417710520188260100',
    #     '10543768020188260100',
    #     '10202861720168260100',
    #     '00069439220118260278',
    #     '10037140520168260320',
    #     '10021883220188260320',
    #     '10702536020188260100',
    #     '10775329720188260100',
    #     '10809703420188260100',
    #     '10819594020188260100',
    #     '10847325820188260100',
    #     '10956753720188260100',
    #     '10026389420188260248',
    #     '11196421420188260100',
    #     '10015330720198260100',
    #     '11288545920188260100',
    #     '10843783320188260100',
    #     '11320070320188260100',
    #     '11279191920188260100',
    #     '10118936720188260348',
    #     '10310271420198260100',
    #     '10310262920198260100',
    #     '10298094820198260100',
    #     '10030532920198260576',
    #     '10509770920198260100',
    #     '10577567720198260100',
    #     '10555127820198260100',
    #     '10261555320198260100',
    #     '10028860520188260428',
    #     '10081715320188260565'
    # ]
    # v = ClassificaMovimento()
    # processo_service = ProcessoService()
    # for i,npu in enumerate(lista):
    #     processos = processo_service.dao.lista_por_numero_processo_ou_npu(npu)
    #     print("numero {i} de {len}".format(i=i,len=len(lista)))
    #     for processo in processos:
    #         movs = processo.movimentos
    #         for m in (movs):
    #             try:
    #                 # if m.processo:
    #                 #     print(m.processo.npu_ou_num_processo + " Processo analisando quadro")
    #                 #v.classifica(m,"DJSP")
    #                 v.verifica_quadro_credores(m,debug=False)
    #             except:
    #                 print("ERRO")