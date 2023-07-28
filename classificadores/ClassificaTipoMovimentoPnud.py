import re
from util.RegexUtil import RegexUtil
import os.path
import subprocess
from classificadores.ClassificadorBase import ClassificadorBase
from pdjus.modelo.Movimento import Movimento
from pdjus.dal.MovimentoDao import MovimentoDao
import csv
from pdjus.service.ProcessoService import ProcessoService

class ClassificaTipoMovimentoPnud(ClassificadorBase):

    def __init__(self, filename):

        novas_colunas = ['sem_merito','parcial_proc', 'improc', 'procedente', 'acordo', 'baixa_definitiva',
                         'citacao','liminar_indeferida','liminar_deferida_parcial','liminar_deferida',
                         'contestacao_apresentada','contestacao_nao_apresentada','defesa_previa','transito_em_julgado',
                         'suspensao_processo_civel','suspensao_processo_penal','sobrestamento','recurso_apelacao_interposta_reu'
            ,'recurso_agravo_retido_interposto_reu' ,'recurso_recurso_adesivo_interposto_reu' ,'recurso_apelacao_interposta_autor'
            ,'recurso_recurso_adesivo_interposto_autor' ,'recurso_agravo_retido_interposto_autor' ,
                         'recurso_embargos_infringentes_apresentados' ,'recurso_apelacao_interposta'
            ,'agravo_de_instrumento_interposto' ,'recurso_recurso_sentido_estrito_interposto' ,'agravo_interno_interposto' ,
                         'recurso_agravo_de_instrumento_apresentado_comprovante_de_interposicao' ,'embargos_de_declaracao_opostos'
            ,'convertido_diligencia','emb_parc_acolhidos','emb_acolhidos','emb_rejeit','extincao_punibilidade','apela_rejeit',
                         'apela_acolhida','apela_parc_acolhida','agrav_acolhido','agravo_rejeit','agrav_parc_acolhidos',
                         'seguranca_concedida','seguranca_rejeit','seguranca_parc_conced']


        super(ClassificaTipoMovimentoPnud, self).__init__(filename, novas_colunas,apaga_arquivo_classificados=False)


    def classifica(self, chunk, index, c):
        chunk = chunk.astype({'sem_merito': str,'parcial_proc': str, 'improc': str, 'procedente': str, 'acordo': str, 'baixa_definitiva': str,
                         'citacao': str,'liminar_indeferida': str,'liminar_deferida_parcial': str,'liminar_deferida': str,
                         'contestacao_apresentada': str,'contestacao_nao_apresentada': str,'defesa_previa': str,'transito_em_julgado': str,
                         'suspensao_processo_civel': str,'suspensao_processo_penal': str,'sobrestamento': str,'recurso_apelacao_interposta_reu'
            : str,'recurso_agravo_retido_interposto_reu' : str,'recurso_recurso_adesivo_interposto_reu' : str,'recurso_apelacao_interposta_autor'
            : str,'recurso_recurso_adesivo_interposto_autor' : str,'recurso_agravo_retido_interposto_autor' : str,
                         'recurso_embargos_infringentes_apresentados' : str,'recurso_apelacao_interposta'
            : str,'agravo_de_instrumento_interposto' : str,'recurso_recurso_sentido_estrito_interposto' : str,'agravo_interno_interposto' : str,
                         'recurso_agravo_de_instrumento_apresentado_comprovante_de_interposicao' : str,'embargos_de_declaracao_opostos'
            : str,'convertido_diligencia': str,'emb_parc_acolhidos': str,'emb_acolhidos': str,'emb_rejeit': str,'extincao_punibilidade': str,'apela_rejeit': str,
                         'apela_acolhida': str,'apela_parc_acolhida': str,'agrav_acolhido': str,'agravo_rejeit': str,'agrav_parc_acolhidos': str,
                         'seguranca_concedida': str,'seguranca_rejeit': str,'seguranca_parc_conced': str})

        #Todos serão classificados pelo tipo movimento, mas alguns eu terei que verificar se ocorreu um tipo para não ocorrer outro. ex embargo acolhido e parcialmente acolhido
        for classe in ['citacao', 'defesa_previa', 'transito_em_julgado', 'suspensao_processo_civel',
                       'suspensao_processo_penal', 'sobrestamento', 'recurso_apelacao_interposta_reu' ,
                       'recurso_agravo_retido_interposto_reu' , 'recurso_recurso_adesivo_interposto_reu' ,
                       'recurso_apelacao_interposta_autor' , 'recurso_recurso_adesivo_interposto_autor' ,
                       'recurso_agravo_retido_interposto_autor' , 'recurso_embargos_infringentes_apresentados' ,
                       'recurso_apelacao_interposta' , 'agravo_de_instrumento_interposto' , 'recurso_recurso_sentido_estrito_interposto' ,
                       'agravo_interno_interposto' , 'recurso_agravo_de_instrumento_apresentado_comprovante_de_interposicao' ,
                       'embargos_de_declaracao_opostos' , 'convertido_diligencia', 'extincao_punibilidade', 'baixa_definitiva']:

            if re.search(RegexUtil.tp_mov_pnud[classe], c['nome']):
                chunk.at[index, classe] = chunk.at[index,'data_movimento']
                self.por_tp += 1

#TODO PARA O TRF2 a baixa definitiva, tem baixa de findo em e baixa de findo. Se tiver EM, verificar no tipo do movimento a data e substituir.

        for classe in ['sem_merito', 'parcial_proc', 'improc', 'procedente', 'acordo']:
            if re.search(RegexUtil.tp_mov_pnud[classe], c['nome']):
                chunk.at[index, classe] = chunk.at[index,'data_movimento']
                self.por_tp += 1
                break

        for classe in ['emb_parc_acolhidos', 'emb_rejeit', 'emb_acolhidos']:
            if re.search(RegexUtil.tp_mov_pnud[classe], c['nome']):
                chunk.at[index, classe] = chunk.at[index,'data_movimento']
                self.por_tp += 1
                break

        for classe in ['contestacao_nao_apresentada','contestacao_apresentada']:
            if re.search(RegexUtil.tp_mov_pnud[classe], c['nome']):
                chunk.at[index, classe] = chunk.at[index,'data_movimento']
                self.por_tp += 1
                break

        for classe in ['apela_parc_acolhida', 'apela_rejeit', 'apela_acolhida']:
            if re.search(RegexUtil.tp_mov_pnud[classe], c['nome']):
                chunk.at[index, classe] = chunk.at[index,'data_movimento']
                self.por_tp += 1
                break


        for classe in ['agrav_acolhido', 'agravo_rejeit']:
            if re.search(RegexUtil.tp_mov_pnud[classe], c['nome']):
                chunk.at[index, classe] = chunk.at[index,'data_movimento']
                self.por_tp += 1
                break

        for classe in ['seguranca_parc_conced', 'seguranca_rejeit', 'seguranca_concedida']:
            if re.search(RegexUtil.tp_mov_pnud[classe], c['nome']):
                chunk.at[index, classe] = chunk.at[index,'data_movimento']
                self.por_tp += 1
                break

        for classe in ['liminar_deferida_parcial', 'liminar_indeferida','liminar_deferida']:
            if re.search(RegexUtil.tp_mov_pnud[classe], c['nome']):
                chunk.at[index, classe] = chunk.at[index,'data_movimento']
                self.por_tp += 1
                break

        return chunk

    def salva(self, chunk, write_header):
        classificados = chunk[(chunk.sem_merito !='0' ) | (chunk.parcial_proc !='0' ) |  (chunk.improc !='0' ) |  (chunk.procedente !='0' )
                              |  (chunk.acordo !='0') | (chunk.baixa_definitiva !='0') | (chunk.citacao !='0' ) |  (chunk.liminar_indeferida !='0' )
                              |  (chunk.liminar_deferida_parcial !='0' ) |  (chunk.liminar_deferida !='0' ) |   (chunk.contestacao_apresentada !='0' )
                              |  (chunk.contestacao_nao_apresentada !='0' ) |  (chunk.defesa_previa !='0' ) |  (chunk.transito_em_julgado !='0' )
                              |  (chunk.suspensao_processo_civel !='0' ) |  (chunk.suspensao_processo_penal !='0' ) |  (chunk.sobrestamento !='0' )
                              |  (chunk.recurso_apelacao_interposta_reu !='0' ) |  (chunk.recurso_agravo_retido_interposto_reu !='0' )
                              |  (chunk.recurso_recurso_adesivo_interposto_reu !='0' ) |  (chunk.recurso_apelacao_interposta_autor !='0' )
                              |  (chunk.recurso_recurso_adesivo_interposto_autor !='0' ) |  (chunk.recurso_agravo_retido_interposto_autor !='0' )
                              |  (chunk.recurso_embargos_infringentes_apresentados !='0' ) |  (chunk.recurso_apelacao_interposta !='0' )
                              |  (chunk.agravo_de_instrumento_interposto !='0' ) |  (chunk.recurso_recurso_sentido_estrito_interposto !='0' )
                              |  (chunk.agravo_interno_interposto !='0' ) |   (chunk.recurso_agravo_de_instrumento_apresentado_comprovante_de_interposicao !='0' )
                              |  (chunk.embargos_de_declaracao_opostos !='0' ) |  (chunk.convertido_diligencia !='0' ) |  (chunk.emb_parc_acolhidos !='0' )
                              |  (chunk.emb_acolhidos !='0' ) |  (chunk.emb_rejeit !='0' ) |  (chunk.extincao_punibilidade !='0' ) |  (chunk.apela_rejeit !='0' )
                              |  (chunk.apela_acolhida !='0' ) |  (chunk.apela_parc_acolhida !='0' ) |  (chunk.agrav_acolhido !='0' )
                              |  (chunk.agravo_rejeit !='0' ) |  (chunk.agrav_parc_acolhidos !='0' ) |   (chunk.seguranca_concedida !='0' )
                              |  (chunk.seguranca_rejeit !='0' ) |  (chunk.seguranca_parc_conced !='0' ) ]

        classificados.to_csv(self.filename.replace('.csv', '') + "-classificados.csv", sep='\t', encoding='utf-8',
                             mode='a', header=write_header, quoting=csv.QUOTE_ALL, quotechar='"', index=False)

if __name__ == '__main__':
    cla = ClassificaTipoMovimentoPnud('reports/out/PNUD_TRF1/tmp-movimentos.csv')
    cla.run(modifica_tipos_para_tipo_movimento=True)