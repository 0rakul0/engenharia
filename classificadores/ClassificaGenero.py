from pdjus.service.ParteService import ParteService
from Name2GenderBR import GenderClassifier

parte_service = ParteService()

k = 0
commit = False
c = GenderClassifier()

for parte in parte_service.dao.lista_parte_sem_genero(inclui_unknown=True):

    if k == 100:
        k = 0
        commit = True

    stats = c.get_stats(parte.nome).fillna(0.0)
    g = c.get_gender(parte.nome)

    if g == 'M' and stats['frequency_female'].get(0)/stats['frequency_male'].get(0) < 0.2 and stats['frequency_total'].get(0) > 150:
        parte.genero = g
    elif g == 'F' and stats['frequency_male'].get(0)/stats['frequency_female'].get(0) < 0.2 and stats['frequency_total'].get(0) > 150:
        parte.genero = g
    else:
        parte.genero = 'U'  # unknown

    print(parte.nome, parte.genero)
    parte_service.salvar(parte, commit=commit)

    k += 1
    commit = False

parte_service.dao.commit()

