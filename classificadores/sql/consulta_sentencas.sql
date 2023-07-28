set search_path='desenv_trf1';

create temp table v1 as select 	p.id processo_id, m.id movimento_id, m.data data_movimento, tm.nome tipo_movimento, m.texto texto_movimento
from	processo p
join	movimento m on m.processo_id = p.id
join	tipo_movimento tm on tm.id = m.tipo_movimento_id
join  classe_processual cp on cp.id = p.classe_processual_id
where 	tm.nome ~ 'INTEIRO_TEOR' and tm.nome ~ 'SENTENCA';

\copy (select * from v1) to 'sentencas.csv' DELIMITER E'\t' CSV HEADER;