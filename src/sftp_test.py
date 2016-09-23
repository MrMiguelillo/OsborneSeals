# 1. descargar zip
# 2. descomprimir
# 3. abrir imágenes una a una
# 4. buscar sello por SURF/ORB
# 5. encuentro? -> clasificar (definir cómo clasificar)
#
# Para SURF/ORB necesito base de datos de sellos:
#     1. Algoritmo de búsqueda de sellos en documentos
#     2. Volver a pasarlo filtrando por color.

# from ftplib import FTP
#
# ftp = FTP('146.255.101.63')
# ftp.login(user='repo', passwd='norevelarjamas')

import paramiko

host = "146.255.101.63"
port = 22
transport = paramiko.Transport((host, port))

password = "norevelarjamas"
username = "repo"
transport.connect(username=username, password=password)

sftp = paramiko.SFTPClient.from_transport(transport)

# path = '/home/repo/Fotos/DSC_0021.JPG'
# localpath = 'C:/Users/usuario/Desktop/DSC_0021.jpg'
# sftp.put(localpath, path)
# sftp.get(path, localpath)



sftp.close()
sftp.close()
print('download done')
