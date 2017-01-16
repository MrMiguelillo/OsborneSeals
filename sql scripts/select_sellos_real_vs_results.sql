select docs_osborne.documentos.sello, docs_osborne.results.sello
from docs_osborne.documentos, docs_osborne.results
where docs_osborne.documentos.ruta = docs_osborne.results.ruta;