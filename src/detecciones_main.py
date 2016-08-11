from src import Detecciones

detectar = Detecciones.Detecciones()

res = detectar.detectar_filas('../imgs/Narciso2.png', 1)
#res = detectar.detectar_filas('../imgs/IMG_0003.png', 2)
print(res)