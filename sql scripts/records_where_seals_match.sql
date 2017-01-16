select docs_osborne.documentos.sello, docs_osborne.results.sello, docs_osborne.results.ratio
from docs_osborne.documentos
inner join docs_osborne.results
on docs_osborne.documentos.ruta = docs_osborne.results.ruta
where docs_osborne.documentos.sello=docs_osborne.results.sello;