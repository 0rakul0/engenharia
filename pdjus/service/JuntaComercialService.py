import re
import json,time
from pdjus.conexao.Conexao import Singleton
from datetime import datetime
from pdjus.dal.JuntaComercialDao import JuntaComercialDao
from pdjus.modelo.JuntaComercial import JuntaComercial
from pdjus.service.BaseService import BaseService
from util.StringUtil import remove_acentos,remove_varios_espacos,remove_caracteres_especiais,remove_links
from classificadores.ClassificaJucesp import ClassificaJucesp



from pdjus.service.EmpresaService import EmpresaService

class JuntaComercialService(BaseService,metaclass=Singleton):

    def __init__(self):
        super(JuntaComercialService, self).__init__(JuntaComercialDao())

    def preenche_junta_comercial(self,nome_empresa,nire,tipo,data,data_caderno,texto,numero_alteracao=None,regex_util=None,lista_cnae=None):
        empresa_service = EmpresaService()
        classifica_jucesp = ClassificaJucesp()

        empresa = empresa_service.preenche_empresa_por_nire(nome_empresa,nire)
        objetos = None
        texto = self.limpa_texto_anotacao(texto)

        empresa._cnpj = None
        if not empresa._cnpj:
            try:
                if re.search('INCLUSAO\s*DE\s*CGC',texto):#Coleta o cnpj da empresa a partir do tipo anotação "Inclusão de CGC"
                    cnpj = re.search('\d{2}\.?\d{3}\.?\d{3}\/?\d{4}\-?\d{2}', texto).group(0)
                    empresa._cnpj = empresa.formata_cnpj(cnpj)
                    empresa_service.salvar(empresa)
                #comentar o trecho abaixo enquanto o mapa de empresas estiver fora
                if not empresa.mapa_verificado:#coleta o mapa da empresa com uma requisiçao ao json da jucesp
                    cnpj,enquadramento,endereco,cep,objetos = self.extrai_json_mapa(empresa.nome,empresa.nire)
                    if cnpj:
                        empresa._cnpj = empresa.formata_cnpj(cnpj)
                    if enquadramento:
                        empresa_service.seta_enquadramento(empresa,enquadramento)
                    if endereco:
                        empresa.endereco = endereco.upper()
                        try:
                            municipio = empresa.endereco.split(',')[-1].split('-')[0]
                            if municipio == '' or municipio == ' ':
                                municipio = empresa.endereco.split(',')[-2]
                                if municipio == '' or municipio == ' ':
                                    print('Empresa de id ', empresa.id, ' não conseguiu extrair endereço')

                        except:
                            print('Não foi possível extrair o municipio da empresa')

                    if cep:
                        empresa.cep = cep
                    empresa.mapa_verificado = True
                    empresa_service.salvar(empresa)
            except:
                print("Não foi possível extrair o CNPJ")

        #Área para inserir o objeto social e classificação do cnae
        if re.search("CONSTI",tipo.nome):
            if len(texto) > 5:#Seta o objeto social da empresa e trata o cnae
                empresa_service.seta_objeto_social(empresa,texto,'1',True,lista_cnae)
        # Comentado o trecho abaixo enquanto o mapa de empresas estiver fora
        if objetos:
            for count, objeto in enumerate(re.split('#|;', objetos)):
                if len(objeto)> 3:
                    if count == 0:
                        empresa_service.seta_objeto_social(empresa,objeto,'0',True,lista_cnae)
                    else:
                        empresa_service.seta_objeto_social(empresa,objeto,'0',False,lista_cnae)

        if type(data) != datetime:
            data = datetime.strptime(data, "%d/%m/%Y").date()

        junta_comercial = self.dao.get_por_empresa_tipo_data_e_texto(empresa, tipo, data, texto)
        if not junta_comercial:
            junta_comercial = JuntaComercial()
            junta_comercial.empresa = empresa
            junta_comercial.tipo_junta = tipo
            junta_comercial.data = data
            junta_comercial.data_caderno = data_caderno
            junta_comercial.texto = texto
            if numero_alteracao:
                try:
                    junta_comercial.numero_alteracao = remove_varios_espacos(remove_caracteres_especiais(numero_alteracao.split(":")[1]))
                except IndexError:
                    junta_comercial.numero_alteracao =  remove_varios_espacos(remove_caracteres_especiais(numero_alteracao))
                except:
                    junta_comercial.numero_alteracao = 'NUMERO INVALIDO'
            self.dao.salvar(junta_comercial,commit=True, salvar_estrangeiras=False,salvar_many_to_many=False)

            if texto != '':#Classifica a anotaçao da jucesp
                constituicao = False
                if re.search("CONSTIT", tipo.nome):
                    constituicao = True
                classifica_jucesp.classica_anotacao(junta_comercial,regex_util,constituicao)

            # if regex_npu:
            #     self.dao.execute_sql(
            #         '''
            #         insert into desenv_t jsp.proc_temp (numero,tag_id,dado_entrada) values ('npu extraido',1,id da junta) ''')
            print("Empresa ", empresa.nome, " do tipo ", tipo.nome, " Salva com o texto: ", texto)
        else:
            print("Alteracao já existe no banco")
        return junta_comercial
        #return None

    def limpa_texto_anotacao(self,texto):
        texto = re.sub("(A\s*L\s*T\s*E\s*R\s*A\s*C\s*A\s*O|C\s*O\s*N\s*S\s*T\s*I\s*T\s*U\s*I\s*C\s*A\s*O)\:?\s*(\d\s*\d\s*\/\s*\d\s*\d\s*\/\s*\d\s*\d\s*\d\s*\d)","", texto)
        texto = remove_caracteres_especiais(remove_links(remove_varios_espacos(remove_acentos(texto.upper()))))
        return texto

    def extrai_json_mapa(self,nome_empresa,nire):
        import requests
        s = requests.Session()
        conseguiu = False
        tentativas = 5
        cnpj, enquadramento, endereco, cep, objetos = None,None,None,None,None
        while conseguiu == False or tentativas <=0:
            try:
                pagina = s.get('https://www.jucesponline.sp.gov.br/GeoJson.aspx?nire={nire}&razao=&objeto=&cnpj=&logradouro=&cep=&bairro=&municipio=&uf=SP&bempresaativa=false&filiais=true&offset=0'.format(nire=nire.strip()))
                if pagina.json():
                    conseguiu= True
            except json.decoder.JSONDecodeError as e:
                conseguiu=False
                tentativas -= 1
                time.sleep(2)
        if not conseguiu:
            return False
        for empresa in pagina.json()['featureCollection']['features']:
            if empresa['properties']['NIRE'] == nire:
                cnpj = empresa['properties']['CNPJ']
                enquadramento =  empresa['properties']['Enquadramento']
                endereco = empresa['properties']['Endereco']
                cep = empresa['properties']['CEP']
                objetos = empresa['properties']['Objeto']

        return cnpj,enquadramento,endereco,cep,objetos

