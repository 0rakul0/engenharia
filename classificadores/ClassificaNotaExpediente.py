# -*- coding: utf-8 -*-


import re
from datetime import datetime
from pdjus.service.ProcessoService import ProcessoService
from pdjus.service.SituacaoProcessoService import SituacaoProcessoService


class ClassificaNotaExpediente:
    def __init__(self):
        self.processoService = ProcessoService()
        self.situacao_processo_service = SituacaoProcessoService()

    def valida(self,movimento):
        self.valida_nota_expediente_de_falencia(movimento)
        self.valida_nota_expediente_de_recuperacao_judicial(movimento)

    def busca_e_atualiza_situacao_processo(self, movimento,nome_situacao):
        situacao_processo = self.situacao_processo_service.preenche_situacao_processo(movimento.processo,nome_situacao,movimento.data)

        return situacao_processo

    def verifica_data_situacao_e_salva_processo(self, movimento, situacao_processo):
        if not situacao_processo.data:
            situacao_processo.data = movimento.data
        self.processoService.dao.salvar(movimento.processo)

    def valida_nota_expediente_de_falencia(self, movimento):
        if not movimento.nota_expediente or not movimento.processo.is_processo_falencia_recuperacao_convolacao():
            return
        nota = movimento.nota_expediente
        expressaoFalDecret = re.compile("[Dd][Ee][Cc][Rr][Ee][Tt]([Aa][Dd][AaoO]|[Oo]([Uu])?) *[Aa] *([Ff][Aa][Ll].{1}[Nn][Cc][Ii][Aa]|[Qq][Uu][Ee][Bb][Rr][Aa]) *(EM DATA DE *(\d{1,2}.\d{1,2}.\d{2,4}))?", re.U)
        expressaoDecreto = re.compile("[Dd][Ee][Cc][Rr][Ee][Tt][Oo](?!-[Ll][Ee][Ii])", re.U)
        expressaoEncerramento = re.compile("[Dd][Ee][Cc][Rr][Ee][Tt]([Aa][Dd][AaOo]|[Oo]([Uu])?)[ ]*[OoAa]?[ ]*[Ee][Nn][Cc][Ee][Rr][Rr][Aa]([Dd][OoAa]|[Mm][Ee][Nn][Tt][Oo])", re.U)
        expressaoSindico = re.compile("([Nn][Oo][Mm][Ee][Aa][Dd]([Oo]|[OoAa)[ ]*[OoAa]?[ ]*)([Ss].[Nn][Dd][Ii][Cc][OoAa]|[Aa][Dd][Mm][Ii][Nn]).*)", re.U)
        expressao_convolacao = re.compile("(por )?convol(o|(a[Çç][ãÃ]o)|a(NDO))[ ,]? * a? *(rec((upera[Çç][ãÃ]o)|(\.? *)?)?)? *(jud((icial)|([. ])?)? * (em)? *(fal[êÊ]ncia)?)? *(decreto)? *((em)|a)? *(fal[êÊ]ncia)?", re.IGNORECASE | re.UNICODE)
        expressao_sob_pena = re.compile('sob pena de .*convola[Çç][ãÃ]o.*fal[Êê]ncia', re.IGNORECASE | re.UNICODE)
        expressaoArtigo73I = re.compile("([Aa][Rr][Tt]([Ii][Gg][Oo])?[\.]?[ ]?73)[ ]?[\/]?[,]?[ ]?(([Ii][Nn][Cc])([Ii][Ss][Oo])?)?[\.]?([ \/]*(([Ii][^A-Za-z]|[1]).?|[Pp][Rr][Ii][Mm][Ee][Ii][Rr][Oo]))[ .:;]?", re.U)
        expressaoArtigo73II = re.compile("([Aa][Rr][Tt]([Ii][Gg][Oo])?[\.]?[ ]?73)[ ]?[\/]?[,]?[ ]?(([Ii][Nn][Cc])([Ii][Ss][Oo])?)?[\.]?([ \/]*(([Ii]{2}[^A-Za-z]|[2]).?|[Ss][Ee][Gg][Uu][Nn][Dd][Oo]))[ .:;]?", re.U)
        expressaoArtigo73III = re.compile("([Aa][Rr][Tt]([Ii][Gg][Oo])?[\.]?[ ]?73)[ ]?[\/]?[,]?[ ]?(([Ii][Nn][Cc])([Ii][Ss][Oo])?)?[\.]?([ \/]*(([Ii]{3}[^A-Za-z]|[3]).?|[Tt][Ee][Rr][Cc][Ee][Ii][Rr][Oo]))[ .:;]?", re.U)
        expressaoArtigo73IV = re.compile("([Aa][Rr][Tt]([Ii][Gg][Oo])?[\.]?[ ]?73)[ ]?[\/]?[,]?[ ]?(([Ii][Nn][Cc])([Ii][Ss][Oo])?)?[\.]?([ \/]*(([Ii][Vv][^A-Za-z]|[ ][4]).?|[Qq][Uu][Aa][Rr][Tt][Oo]))[ .:;]?", re.U)
        expressaoArtigo73 = re.compile("([Aa][Rr][Tt]([Ii][Gg][Oo])?[\.]?[ ]?73\D)", re.U)

        if nota.texto:
            decreto_match = expressaoDecreto.search(nota.texto)
            decretacao_falencia_match = expressaoFalDecret.search(nota.texto)
            if decretacao_falencia_match or decreto_match:
                situacao_processo_com_decretacao = self.busca_e_atualiza_situacao_processo(movimento,"DECRETADO")
                if decretacao_falencia_match.group(5) and not situacao_processo_com_decretacao.data:
                    situacao_processo_com_decretacao.data = self.transforma_em_data(decretacao_falencia_match.group(5))
                self.verifica_data_situacao_e_salva_processo(movimento, situacao_processo_com_decretacao)
            else:
                encerramento_match = expressaoEncerramento.search(nota.texto)
                if encerramento_match:
                    situacao_processo_encerrado = self.busca_e_atualiza_situacao_processo(movimento,"ENCERRADO")
                    self.verifica_data_situacao_e_salva_processo(movimento, situacao_processo_encerrado)
                else:
                    sindico_match = expressaoSindico.search(nota.texto)
                    if sindico_match:
                        situacao_processo_nomeado_sindico = self.busca_e_atualiza_situacao_processo(movimento,"NOMEADO SINDICO")
                        self.verifica_data_situacao_e_salva_processo(movimento, situacao_processo_nomeado_sindico)
                    else:
                        sob_pena_match = expressao_sob_pena.search(nota.texto)
                        convolacao_match = expressao_convolacao.search(nota.texto)
                        art73I_match = expressaoArtigo73I.search(nota.texto)
                        art73II_match = expressaoArtigo73II.search(nota.texto)
                        art73III_match = expressaoArtigo73III.search(nota.texto)
                        art73IV_match = expressaoArtigo73IV.search(nota.texto)
                        art73_match = expressaoArtigo73.search(nota.texto)
                        if not sob_pena_match and (convolacao_match or art73_match or art73I_match or art73II_match or art73III_match or art73IV_match):
                            situacao_processo_convolacao = self.busca_e_atualiza_situacao_processo(movimento,"CONVOLACAO")
                            self.verifica_data_situacao_e_salva_processo(movimento, situacao_processo_convolacao)


    def valida_nota_expediente_de_recuperacao_judicial(self,movimento):
        if not movimento.nota_expediente or (not movimento.processo.is_processo_da_classe_ou_assunto('falencia')
                                             or movimento.processo.is_processo_da_classe_ou_assunto('recuperacao')) :
            return
        else:
            nota = movimento.nota_expediente
        expressao_defer_rec_jud = re.compile("(?<![Nn].[Oo]) *(?<![Ii][Nn])([Dd][Ee][Ff][EeIi][Rr][A-Za-z]* *[Dd]?[OoAa]? *([Pp][Rr][Oo][Cc][Ee][Ss][Ss][A-Za-z]*)( *[Dd][AaOo] *[Pp][Ee][Dd][Ii][Dd][Oo])? * *[Dd]?[OoAaEe]? *[Rr][Ee][Cc][Uu][Pp][Ee][Rr][Aa][ÇçCc][AaÃã][Oo] *[Jj][Uu][Dd][Ii][Cc][Ii][Aa][Ll])", re.UNICODE)
        expressao_concessao = re.compile("([Cc][Oo][Nn][Cc][Ee]\D{2,4}[ ]*.{0,6}([Pp][Ee][Dd][Ii][Dd][Oo][ ]*.{0,6})?[Rr][Ee][Cc][Uu][Pp][Ee][Rr][Aa]..[Oo][ ]*[Jj][Uu][Dd][Ii][Cc][Ii][Aa][Ll])[ ]*", re.UNICODE)
        expressaoDecretacao = re.compile("([D][E][C][R][E][T]([Aa][Dd][AaoO]|[Oo]([Uu])?)[ ]*[OoAa]?[ ]*[R][E]|[C][U][P][E][R][A]..[O][ ]*[J][U]|[D][U][I][C][I][A][L])[ ]*(.*)", re.U)
        expressao_convolacao = re.compile("(por )?convol(o|(a[Çç][ãÃ]o)|a(NDO))[ ,]? * a? *(rec((upera[Çç][ãÃ]o)|(\.? *)?)?)? *(jud((icial)|([. ])?)? * (em)? *(fal[êÊ]ncia)?)? *(decreto)? *((em)|a)? *(fal[êÊ]ncia)?", re.IGNORECASE | re.UNICODE)
        expressao_sob_pena = re.compile('sob pena de .*convola[Çç][ãÃ]o.*fal[Êê]ncia', re.IGNORECASE | re.UNICODE)
        expressaoEncerramento = re.compile("[Dd][Ee][Cc][Rr][Ee][Tt]([Aa][Dd][AaOo]|[Oo]([Uu])?)[ ]*[OoAa]?[ ]*[Ee][Nn][Cc][Ee][Rr][Rr][Aa]([Dd][OoAa]|[Mm][Ee][Nn][Tt][Oo])", re.U)
        expressaoArtigo52 = re.compile("([Aa][Rr][Tt]([Ii][Gg][Oo])?[\.]?[ ]?52\D[.]*)", re.U)
        expressaoArtigo73I = re.compile("([Aa][Rr][Tt]([Ii][Gg][Oo])?[\.]?[ ]?73)[ ]?[\/]?[,]?[ ]?(([Ii][Nn][Cc])([Ii][Ss][Oo])?)?[\.]?([ \/]*(([Ii][^A-Za-z]|[1]).?|[Pp][Rr][Ii][Mm][Ee][Ii][Rr][Oo]))[ .:;]?", re.U)
        expressaoArtigo73II = re.compile("[^(sob pena de decreta)].*([Aa][Rr][Tt]([Ii][Gg][Oo])?[\.]?[ ]?73)[ ]?[\/]?[,]?[ ]?(([Ii][Nn][Cc])([Ii][Ss][Oo])?)?[\.]?([ \/]*(([Ii]{2}[^A-Za-z]|[2]).?|[Ss][Ee][Gg][Uu][Nn][Dd][Oo]))[ .:;]?", re.U)
        expressaoArtigo73III = re.compile("([Aa][Rr][Tt]([Ii][Gg][Oo])?[\.]?[ ]?73)[ ]?[\/]?[,]?[ ]?(([Ii][Nn][Cc])([Ii][Ss][Oo])?)?[\.]?([ \/]*(([Ii]{3}[^A-Za-z]|[3]).?|[Tt][Ee][Rr][Cc][Ee][Ii][Rr][Oo]))[ .:;]?", re.U)
        expressaoArtigo73IV = re.compile("([Aa][Rr][Tt]([Ii][Gg][Oo])?[\.]?[ ]?73)[ ]?[\/]?[,]?[ ]?(([Ii][Nn][Cc])([Ii][Ss][Oo])?)?[\.]?([ \/]*(([Ii][Vv][^A-Za-z]|[ ][4]).?|[Qq][Uu][Aa][Rr][Tt][Oo]))[ .:;]?", re.U)
        expressaoArtigo73 = re.compile("([Aa][Rr][Tt]([Ii][Gg][Oo])?[\.]?[ ]?73\D)", re.U)
        expressaoArtigo58 = re.compile("([Aa][Rr][Tt]([Ii][Gg][Oo])?[\.]?[ ]?58\D)", re.U)
        expressaoArtigo63 = re.compile("([Aa][Rr][Tt]([Ii][Gg][Oo])?[\.]?[ ]?63\D)", re.U)

        deferimento_proc_match = expressao_defer_rec_jud.search(nota.texto)
        art52_match = expressaoArtigo52.search(nota.texto)
        concessao_match= expressao_concessao.search(nota.texto)
        convolacao_match = expressao_convolacao.search(nota.texto)
        sob_pena_match = expressao_sob_pena.search(nota.texto)
        encerramento_match = expressaoEncerramento.search(nota.texto)
        decretacao_match= expressaoDecretacao.search(nota.texto)
        art73I_match = expressaoArtigo73I.search(nota.texto)
        art73II_match = expressaoArtigo73II.search(nota.texto)
        art73III_match = expressaoArtigo73III.search(nota.texto)
        art73IV_match = expressaoArtigo73IV.search(nota.texto)
        art73_match = expressaoArtigo73.search(nota.texto)
        art58_match = expressaoArtigo58.search(nota.texto)
        art63_match = expressaoArtigo63.search(nota.texto)

        if deferimento_proc_match or concessao_match or decretacao_match or art58_match or (art52_match and not 'INDEFERIDO' in nota.texto.upper()):
            situacao_processo_com_defer_proc = self.busca_e_atualiza_situacao_processo(movimento,"DEFERIDO")
            self.verifica_data_situacao_e_salva_processo(movimento, situacao_processo_com_defer_proc)

        elif not sob_pena_match and (convolacao_match or art73_match or art73I_match or art73II_match or art73III_match or art73IV_match):
            situacao_processo_com_convolacao = self.busca_e_atualiza_situacao_processo(movimento,"CONVOLACAO")
            self.verifica_data_situacao_e_salva_processo(movimento, situacao_processo_com_convolacao)

        elif encerramento_match or art63_match:
            situacao_processo_encerrado = self.busca_e_atualiza_situacao_processo(movimento,"ENCERRADO")
            self.verifica_data_situacao_e_salva_processo(movimento, situacao_processo_encerrado)


    def transforma_em_data(self,input):
        data = datetime.strptime(input, "%d/%m/%Y")
        return data





