select docs_osborne.ground_truth.sello, docs_osborne.results4.sello, docs_osborne.results4.ratio
from docs_osborne.ground_truth
inner join docs_osborne.results4
on substring(docs_osborne.ground_truth.ruta, 34, 999) = substring(docs_osborne.results4.ruta, 21, 999)
where docs_osborne.ground_truth.sello=docs_osborne.results4.sello;