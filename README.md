v0.1
----------
1. Creado gui_test para saber cómo se usan la funcionalidad gui de opencv
2. Creado bin_test para obtener parámetros de umbralización óptimos
3. Creado opening_test para ver si un opening soluciona el ruido de la 
umbralización adaptativa -> no lo hace
4. Creado hist_vert para test separación en líneas
5. Creado hist_horiz para test de separación de columnas
6. main es el futuro programa final, de momento no es útil

----------
v0.2
1. README ya es funcional

----------
v0.3
1. Movidas las funciones de histogramas proyectados al archivo Splitting.py
2. Actualizados hist_vert.py y hist_horiz.py para usar las nuevas funciones

----------
v0.3.1
1. Añadido .gitignore

----------
v0.4
1. Creacion de la clase umbralizado y la funcion de umbralizar
2. Tocada el archivo bin_test en relacion funcion umbralizar

----------
v0.4.1
1. Cambio de las direcciones donde se encuentran las imagenes

----------
v0.5.1
1. Se elimina Splitting y se traducen funciones relacionadas

----------
v0.5.2
1. Se corrige la función separar_columnas para incluir el argumento self

----------
v0.5.3
1. Se cambian los nombres de la clase Umbralizacion y la clase bin_test a español

----------
v0.5.4
1. Se actualiza .gitignore

----------
v0.5.5
1. Se cambia Separar.separar_columnas() a Separar.columnas()