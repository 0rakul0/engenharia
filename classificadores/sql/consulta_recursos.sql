set search_path='pnud';

create temp table v1 as
select  p.id processo_id, m.id movimento_id, m.data data_movimento, tm.nome tipo_movimento, m.texto texto_movimento
from processo p
join movimento m on m.processo_id = p.id
join tipo_movimento tm on tm.id = m.tipo_movimento_id
-- incluir aqui a classe processual???
where  tm.nome ~ 'INTEIRO_TEOR' and tm.nome ~ '(AGRAVO\s*DE\s*INSTRUMENTO\s*(EM\s*RECURSO\s*(ESPECIAL|EXTRAORDINARIO))?)|RECURSO(DES)?PROVIDO|MONOCRAT|((APELACAO)\s*\/\s*REMESSA\s*NECESSARIA)|APELACAO|REMESSA\s*NECESSARIA\s*|MANDADO\s*DE\s*SEGURANCA|(RECURSO\s*(INOMINADO|DE\s*MEDIDA\s*CAUTELAR))|ACORDAO';

\copy (select * from v1) to 'pnud-recursos.dat' DELIMITER E'\t' CSV HEADER;