select docs_osborne.documentos.sello, docs_osborne.results.sello, docs_osborne.results.ratio, docs_osborne.documentos.ruta
from docs_osborne.documentos, docs_osborne.results
where docs_osborne.documentos.ruta = docs_osborne.results.ruta;