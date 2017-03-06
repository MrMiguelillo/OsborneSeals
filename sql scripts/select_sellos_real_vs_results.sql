select docs_osborne.ground_truth.sello, docs_osborne.results4.sello, docs_osborne.results4.ratio, docs_osborne.ground_truth.ruta
from docs_osborne.ground_truth, docs_osborne.results4
where substring(docs_osborne.ground_truth.ruta, 34, 999) = substring(docs_osborne.results4.ruta, 21, 999)