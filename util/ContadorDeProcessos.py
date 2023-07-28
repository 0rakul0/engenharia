import re

busca = re.compile('PROCESSO SALVO')
apensado = re.compile('salvo o apensado \d{6,7}')
subprocesso = re.compile('salvo subprocesso')
com_senha = re.compile('com senha:')
incidente = re.compile('salvo incidente')
sem_processo = re.compile('nao tem processo')

palavra_count = 0
apensado_count = 0
subprocesso_count = 0
com_senha_count = 0
incidente_count = 0
sem_processo_count = 0

with open(r'C:\Users\b13001972777\Documents\falencias_segundo_grau\salvos.txt') as arq:
    arquivo = arq.readlines()
    for line in arquivo:
        if busca.search(line):
            palavra_count +=1
        elif apensado.search(line):
            apensado_count +=1
            sem_processo_count -=1
        elif com_senha.search(line):
            com_senha_count +=1
        elif subprocesso.search(line):
            subprocesso_count +=1
            # palavra_count -=1
        elif incidente.search(line):
            incidente_count +=1
        elif sem_processo.search(line):
            sem_processo_count +=1

total = palavra_count + apensado_count + subprocesso_count + com_senha_count + incidente_count + sem_processo_count

print('prcesso salvo',palavra_count)
print('apensados salvos', apensado_count)
print('com senha', com_senha_count)
print('subprocessos', subprocesso_count)
print('incidente', incidente_count)
print('sem processo', sem_processo_count)

print(total)