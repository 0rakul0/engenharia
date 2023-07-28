import pandas as pd


dataframe_recursos_666 = pd.read_csv(r'C:\Users\b13001972777\Documents\PycharmProjects\IpeaJUS\dados\recursos_sem_mono_sem_julg.csv')
dataframe_revisto_303 = pd.read_csv(r'C:\Users\b13001972777\Documents\PycharmProjects\IpeaJUS\dados\julgamentos_info.csv')


lista_recursos_total = []
lista_revisto = []

for linha in dataframe_recursos_666['npu']:
    lista_recursos_total.append(linha)

for lin in dataframe_revisto_303['NPU']:
    lista_revisto.append(lin)

restos = set(lista_recursos_total).difference(set(lista_revisto))

print(restos)
print(len(lista_revisto))
print(len(set(lista_revisto)))
print(len(lista_recursos_total))
print(len(set(lista_recursos_total)))
print(len(restos))