from unittest import TestCase
import abc

from util.StringUtil import remove_acentos, remove_varios_espacos


class test_AcompanhamentoBase(TestCase,metaclass=abc.ABCMeta):


    def generico_gera_arvore_processo(self,acompanhamento,npu=None,numero_processo=None,orgao_julgador=None,advogados=None,comarca=None, classe_processual=None, assunto=None, juiz=None, partes= [] , movimentos = [],tag=None,caderno=None):
        if npu:
            processo = acompanhamento.gera_arvore_processos(npu, tag, False, caderno)
        if numero_processo:
            processo = acompanhamento.gera_arvore_processos(numero_processo, tag, False, caderno)

        self.assertTrue(processo)
        self.assertTrue(processo.id)

        if npu:
            self.assertEqual(npu,processo.npu)
        if orgao_julgador:
            self.assertEqual(remove_varios_espacos(remove_acentos(orgao_julgador.upper())),processo.orgao_julgador)
        if advogados:
            nomes_advogados = list([advogado.nome for advogado in processo.advogados])
            for advogado in nomes_advogados:
                self.assertIn(remove_varios_espacos(remove_acentos(advogado.upper())),advogados)
        if numero_processo:
            self.assertEqual(numero_processo,processo.numero_processo)
        if classe_processual:
            self.assertTrue(processo.classe_processual.id)
            self.assertEqual(remove_varios_espacos(remove_acentos(classe_processual.upper())),processo.classe_processual.nome)
        if assunto:
            assuntos = list([assunto.nome for assunto in processo.assuntos])
            self.assertIn(remove_varios_espacos(remove_acentos(assunto.upper())),assuntos)
        if juiz:
            self.assertTrue(processo.juiz.id)
            self.assertEqual(remove_varios_espacos(remove_acentos(juiz.upper())), processo.juiz.nome)
        if comarca:
            self.assertTrue(processo.reparticao.comarca.id)
            self.assertEqual(remove_varios_espacos(remove_acentos(comarca.upper())), processo.reparticao.comarca.nome)
        if partes:
            nomes_partes = list([parte.nome for parte in processo.partes])
            for parte in partes:
                self.assertIn(remove_varios_espacos(remove_acentos(parte.upper())), nomes_partes)
        if movimentos:
            texto_movimentos = list([movimento.texto for movimento in processo.movimentos])
            for movimento in movimentos:
                self.assertIn(remove_varios_espacos(remove_acentos(movimento.upper())), texto_movimentos)
        if tag:
            tags = list([tag.marcador for tag in processo.dado_extraido.historicos])
            self.assertIn(remove_varios_espacos(remove_acentos(tag.upper())), tags)
        if caderno:
            cadernos = list([tag.caderno for tag in processo.dado_extraido.historicos])
            self.assertIn(caderno, cadernos)





