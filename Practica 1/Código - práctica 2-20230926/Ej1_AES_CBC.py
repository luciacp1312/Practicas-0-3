from Crypto.Random import get_random_bytes
from Crypto.Cipher import DES, AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Util import Counter

# Datos necesarios
key = get_random_bytes(16)  # Clave aleatoria de 64 bits
IV = get_random_bytes(16)  # IV aleatorio de 64 bits
BLOCK_SIZE_AES = 16  # Bloque de 64 bits
data1 = "Hola Amigos de Seguridad" #\xc3\x04\x02W\x90\xac\x8f\x81!\xac\xe3\xc4\x84\x12PMDj\xb3CC@\xa8\xae'LPu\reo
data2 = "Hola Amigas de Seguridad"
# l\xcf\xadn*u\xeb\xb1\x91\xea(a\x13\x91\xe4<,M\xad0$\x1f\xd7\xcbVY8\xb1\xa9\x1fp%
data = data1.encode("utf-8")

# data = "Hola Mundo con DES en modo CBC".encode("utf-8")  # Datos a cifrar
print(data)

# CIFRADO ##########################################################################

# Creamos un mecanismo de cifrado DES en modo CBC con un vector de inicialización IV
cipher = AES.new(key, AES.MODE_CBC, IV)

# Ciframos, haciendo que la variable “data” sea múltiplo del tamaño de bloque
ciphertext = cipher.encrypt(pad(data, BLOCK_SIZE_AES))

# Mostramos el cifrado por pantalla en modo binario
print(ciphertext)

# DESCIFRADO #######################################################################

# Creamos un mecanismo de (des)cifrado DES en modo CBC con una inicializacion IV
# Ambos, cifrado y descifrado, se crean de la misma forma
decipher_des = AES.new(key, AES.MODE_CBC, IV)

# Desciframos, eliminamos el padding, y recuperamos la cadena
new_data = unpad(decipher_des.decrypt(ciphertext),
                 BLOCK_SIZE_AES).decode("utf-8", "ignore")

# Imprimimos los datos descifrados
print(new_data)
