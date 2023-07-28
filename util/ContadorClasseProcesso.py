
import re

# compile
agravo_intrumento = re.compile('AGRAVO DE INSTRUMENTO')
agravo_regimental_civil = re.compile('AGRAVO REGIMENTAL CIVEL')
agravo_interno_civil = re.compile('AGRAVO INTERNO CIVEL')
apelacao_civil = re.compile('APELACAO CIVEL')
conflito_de_competencia_civil = re.compile('CONFLITO DE COMPETENCIA CIVEL')
comprimento_de_sentenca = re.compile('CUMPRIMENTO DE SENTENCA')
embargos_de_declaracao_civil = re.compile('EMBARGOS DE DECLARACAO CIVEL')
habilitacao = re.compile('HABILITACAO')
mandado_de_seguranca_civil = re.compile('MANDADO DE SEGURANCA CIVEL')
recurso_sem_sentido_estrito = re.compile('RECURSO EM SENTIDO ESTRITO')


# contador
agravo_intrumento_count = 0
agravo_regimental_civil_count = 0
agravo_interno_civil_count = 0
apelacao_civil_count = 0
conflito_de_competencia_civil_count = 0
comprimento_de_sentenca_count = 0
embargos_de_declaracao_civil_count = 0
habilitacao_count = 0
mandado_de_seguranca_civil_count = 0
recurso_sem_sentido_estrito_count = 0

# leitura do arquivo
with open(r'C:\Users\b13001972777\Documents\falencias_segundo_grau\classe_processual.txt') as arq:
    arquivo = arq.readlines()
    for line in arquivo:
        # line = line.replace('\n', '_')
        if agravo_intrumento.search(line):
            agravo_intrumento_count +=1
        elif agravo_regimental_civil.search(line):
            agravo_regimental_civil_count += 1
        elif agravo_interno_civil.search(line):
            agravo_interno_civil_count += 1
        elif apelacao_civil.search(line):
            apelacao_civil_count +=1
        elif comprimento_de_sentenca.search(line):
            comprimento_de_sentenca_count += 1
        elif conflito_de_competencia_civil.search(line):
            conflito_de_competencia_civil_count += 1
        elif embargos_de_declaracao_civil.search(line):
            embargos_de_declaracao_civil_count += 1
        elif habilitacao.search(line):
            habilitacao_count += 1
        elif mandado_de_seguranca_civil.search(line):
            mandado_de_seguranca_civil_count += 1
        elif recurso_sem_sentido_estrito.search(line):
            recurso_sem_sentido_estrito_count += 1


soma_total = agravo_interno_civil_count + agravo_intrumento_count + agravo_regimental_civil_count + apelacao_civil_count + conflito_de_competencia_civil_count + comprimento_de_sentenca_count + recurso_sem_sentido_estrito_count + habilitacao_count + mandado_de_seguranca_civil_count
# contadores
print('agravo instrumento: ',agravo_intrumento_count)
print('agravo regimental civil: ', agravo_regimental_civil_count)
print('agravo interno civil: ', agravo_interno_civil_count)
print('apelação civil: ', apelacao_civil_count)
print('conflito de competencia civil: ', conflito_de_competencia_civil_count)
print('comprimento de sentenca: ', comprimento_de_sentenca_count)
print('embargos de declaracao civil: ', embargos_de_declaracao_civil_count)
print('habilitação: ', habilitacao_count)
print('mandado de segurança civil: ', mandado_de_seguranca_civil_count)
print('recurso sem sentido estrito: ', recurso_sem_sentido_estrito_count)
print('############ total ###############')
print('com classe: ', soma_total)
