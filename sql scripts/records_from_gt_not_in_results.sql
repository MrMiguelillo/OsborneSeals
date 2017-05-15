select *
from docs_osborne.ground_truth
left join docs_osborne.heur_results1
on substring(docs_osborne.ground_truth.ruta, 34, 999) = substring(docs_osborne.heur_results1.ruta, 21, 999)
where substring(docs_osborne.heur_results1.ruta, 21, 999) is null