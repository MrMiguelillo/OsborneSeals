import cv2
import matplotlib.pyplot as plt

texto = []
pagina = []
documento = []
with open('../1882-L123.M17.T_2.txt') as inputfile:
    for line in inputfile:
        #texto.append(line.strip().split('\t'))
        texto.append(line.strip())

for z in range (1, len(texto)):
    if texto[z] == "..........":
        documento.append(pagina)
        pagina = []
    else:
        pagina.append(texto[z])

