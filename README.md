Readme Lab Osborne JMC, MRL, RRG, JSM
================== 

v1.1.1 (RRG)
------------
1. Pruebas para unir componentes conexas en distintas lineas

v1.1.0 (RRG)
------------
1. Se detectan correctamente las palabras por el método de las componenetes conexas

v1.0.2 (RRG)
------------
1. Cambios en main_componentes_conexas para hacer pruebas con el erosionado

v1.0.1 (RRG)
------------
1. Nuevo main_componentes_conexas
2. Modificadas las funciones que realizan los histogramas con numpy

v0.7.5 (RRG)
------------
1. Pruebas con la función separar.ajustar para ajustar las palabras
2. Modificada la función main_palabras

v0.7.4 (RRG)
------------
1. La función main_palabras funciona correctamente
2. Modificada la función Separación.ajustar para funcionar con palabras que se solapan

v0.7.3 (JMC)
------------
1. Creada función ajustar para las palabras, no furrula

v0.7.2 (RRG)
-------------
1. Creada funcion main_palabras. Ahora guardamos las coordenadas de los dos puntos que limitan cada palabra

v0.7.1 (RRG)
-------------
1. Modificado el nombre de salida de las imagenes en bin_test
2. Modificado el nombre de las imágenes binarizadas

v0.7.0 (JMC)
-------------
1. Main_simple funciona de forma correcta, la imagen resultada es salida2

v0.6.17 (JMC)
-------------
1. Modificada main_simple sin exito

v0.6.16 (JMC)
-------------
1. Añadida imagen Narciso1 y umbralizada met1,vec0,sig0,thr143
2. Modificado archivo main_ramon y bin_test
3. Añadido main_simple para imagenes en una sola columna

v0.6.15 (RRG)
-------------
1. main_ramon ahora separa ambas partes de la imagen.

v0.6.14 (JMC)
-------------
1. Cambiado el orden del Readme y añadidos los autores. 

v0.6.13 (RRG)
-------------
1. Mejora de la salida de datos en main_ramon.

v0.6.12 (RRG)
-------------
1. Separacion.palabras añade tamaño mínimo de palabras.

v0.6.11 (RRG)
-------------
1. Separación de palabras hecha pero da mal resultado. main_ramon modificado.

v0.6.10  (RRG)
--------------
1. Función Separacion.filas correcta. Si no hay pasos por cero, hace la media entre dos puntos.

v0.6.9  (JMC)
-------------
1. Cambios en Separacion.filas.
2. Subidas fotos nuevas.

v0.6.8 
------
1. Cambiado salida de filtros para que sean tipo ndarray.
2. Cambiado main_ramon acorde con el cambio 1.
3. Corregido main ramon para usar el nuevo nombre de filtro.mediana.

v0.6.7
----------
1. Cambiado salida de filtros para que sean tipo ndarray.
2. Cambiado main_ramon acorde con el cambio 1.
3. Corregido main ramon para usar el nuevo nombre de filtro.mediana.

v0.6.6
----------
1. Muestra separación de líneas en main_ramon.

v0.6.5
----------
1. Mejorar salida int funcion Separacion.filas

v0.6.4
----------
1. Borrar variable rango en la funcion media.

v0.6.3
----------
1. Refactorizadas filtro_media y filtro_mediana.
2. Eliminado max_factor de Filtros.py.
3. Refactorizado datos por histograma en filtro_media(media).

v0.6.2
----------
1. Añadida funcion filas en Separacion.py.

v0.6.1
----------
1. Añadido archivo Filtros.py con funciones de filtros.
2. Borrado los filtros del archivo Separacion.py.
3. Modificado el archivo hist_vert añadiendo las relaciones de Filtros.py.

v0.6
----------
1. hist_vert ahora utiliza el filtro de mediana.

v0.5.6
----------
1. Comentadas funciones de columnas y filtro mediana.
2. average_smoothing -> filtro_media.
3. filtro_media movido a Separación.py.
4. Solucionado bug de filtro de media.

v0.5.5
----------
1. Se cambia Separar.separar_columnas() a Separar.columnas().

v0.5.4
----------
1. Se actualiza .gitignore.

v0.5.3
----------
1. Se cambian los nombres de la clase Umbralizacion y la clase bin_test a español.

v0.5.2
----------
1. Se corrige la función separar_columnas para incluir el argumento self.

v0.5.1
----------
1. Se elimina Splitting y se traducen funciones relacionadas.

v0.4.1
----------
1. Cambio de las direcciones donde se encuentran las imagenes.

v0.4
----------
1. Creacion de la clase umbralizado y la funcion de umbralizar.
2. Tocada el archivo bin_test en relacion funcion umbralizar.

v0.3.1
----------
1. Añadido .gitignore.

v0.3
----------
1. Movidas las funciones de histogramas proyectados al archivo Splitting.py.
2. Actualizados hist_vert.py y hist_horiz.py para usar las nuevas funciones.

v0.2
----------
1. README ya es funcional.

v0.1
----------
1. Creado gui_test para saber cómo se usan la funcionalidad gui de opencv.
2. Creado bin_test para obtener parámetros de umbralización óptimos.
3. Creado opening_test para ver si un opening soluciona el ruido de la.
umbralización adaptativa -> no lo hace.
4. Creado hist_vert para test separación en líneas.
5. Creado hist_horiz para test de separación de columnas.
6. main es el futuro programa final, de momento no es útil.
