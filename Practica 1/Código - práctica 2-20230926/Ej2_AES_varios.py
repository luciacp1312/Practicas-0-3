from Crypto.Random import get_random_bytes
from Crypto.Cipher import DES, AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Util import Counter

# Datos necesarios
key = get_random_bytes(16)  # Clave aleatoria de 128 bits
nonce = get_random_bytes(8)  # IV aleatorio de 64 bits
IV_16 = get_random_bytes(16)  # IV aleatorio de 128 bits
BLOCK_SIZE_AES = 16  # Bloque de 128 bits
mac_len = 16
data = "Hola Amigos de Seguridad".encode("utf-8")
print(data)

# CIFRADO ##########################################################################

# Creamos un mecanismo de cifrado DES en modo CBC con un vector de inicialización IV
# cipher = DES.new(key, DES.MODE_CBC, IV_16) # CBC
# cipher = AES.new(key, AES.MODE_ECB)  # ECB
# cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)  # CTR
# cipher = AES.new(key, AES.MODE_OFB, IV_16)  # OFB
# cipher = AES.new(key, AES.MODE_CFB, IV_16)  # CFB
cipher = AES.new(key, AES.MODE_GCM, nonce = IV_16)  # GCM

# Ciframos, haciendo que la variable “data” sea múltiplo del tamaño de bloque
# ciphertext = cipher.encrypt(pad(data, BLOCK_SIZE_AES))  # ECB, CTR, OFB, CFB
ciphertext,mac_cifrado = cipher.encrypt_and_digest(pad(data,BLOCK_SIZE_AES)) # SOLO GCM
# Mostramos el cifrado por pantalla en modo binario
print(ciphertext)

# DESCIFRADO #######################################################################

# Creamos un mecanismo de (des)cifrado DES en modo CBC con una inicializacion IV
# Ambos, cifrado y descifrado, se crean de la misma forma
# decipher_des = DES.new(key, DES.MODE_CBC, IV_16)
# decipher_aes = AES.new(key, AES.MODE_ECB)  # ECB
# decipher_aes = AES.new(key, AES.MODE_CTR, nonce=nonce)  # CTR
# decipher_aes = AES.new(key, AES.MODE_OFB, IV_16)  # OFB
# decipher_aes = AES.new(key, AES.MODE_CFB, IV_16)  # CFB
# Desciframos, eliminamos el padding, y recuperamos la cadena
# new_data = unpad(decipher_aes.decrypt(ciphertext), BLOCK_SIZE_AES).decode("utf-8", "ignore")  # ECB, CTR, OFB, CFB

# SOLO PARA GCM
decipher_aes = AES.new(key, AES.MODE_GCM, nonce = IV_16)
try:
    new_data=unpad(decipher_aes.decrypt_and_verify(ciphertext, mac_cifrado), BLOCK_SIZE_AES).decode("utf-8", "ignore")
    print(new_data)
except (ValueError, KeyError) as e:
    print("ERROR")
    


# Imprimimos los datos descifrados
# print(new_data) # ECB, CTR, OFB, CFB
