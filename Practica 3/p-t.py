from Crypto.Hash import SHA256, HMAC
import base64
import json
import sys
from socket_class import SOCKET_SIMPLE_TCP
import funciones_aes

# Paso 0: Crea las claves que T comparte con B y A
##################################################

# Crear Clave KAT, guardar a fichero
KAT = funciones_aes.crear_AESKey()
FAT = open("KAT.bin", "wb")
FAT.write(KAT)
FAT.close()

# Crear Clave KBT, guardar a fichero
KBT = funciones_aes.crear_AESKey()
FBT = open("KBT.bin", "wb")
FBT.write(KBT)
FBT.close()

# Paso 1) B->T: KBT(Bob, Nb) en AES-GCM
#######################################

# Crear el socket de escucha de Bob (5551)
print("Esperando a Bob...")
socket_Bob = SOCKET_SIMPLE_TCP('127.0.0.1', 5551)
socket_Bob.escuchar()

# Crea la respuesta para B y A: K1 y K2
K1 = funciones_aes.crear_AESKey()
K2 = funciones_aes.crear_AESKey()

# Recibe el mensaje
cifrado = socket_Bob.recibir()
cifrado_mac = socket_Bob.recibir()
cifrado_nonce = socket_Bob.recibir()

# Descifro los datos con AES GCM
datos_descifrado_ET = funciones_aes.descifrarAES_GCM(KBT, cifrado_nonce, cifrado, cifrado_mac)

# Decodifica el contenido: Bob, Nb
json_ET = datos_descifrado_ET.decode("utf-8" ,"ignore") # ignore = si un caracter no puede decodificarse lo omite, no lanza error
print("B -> T (descifrado): " + json_ET)
msg_ET = json.loads(json_ET)

# Extraigo el contenido
t_bob, t_nb = msg_ET
t_nb = bytearray.fromhex(t_nb) # lo convierte en bytearray
# No comprueba directamente el nonce que recibe de B (sin cifrar) con el que recibe en el mensaje cifrado
# Esto se debe a que ya lo hace dentro de GCM (tambien comprueba el mac dentro)

# Paso 2) T->B: KBT(K1, K2, Nb) en AES-GCM
##########################################
# (A realizar por el alumno/a...)
# Creo el mensaje con las claves y el nonce de B
msg_TB = []
msg_TB.append(K1.hex())
msg_TB.append(K2.hex())
msg_TB.append(t_nb.hex())
json_TB = json.dumps(msg_TB)
print("T -> B (cifrado): " + json_TB)

# Cifro en mensaje
aes_cifB = funciones_aes.iniciarAES_GCM(KBT)
msg_cifB, mac_cifB, nonce_cifB = funciones_aes.cifrarAES_GCM(aes_cifB, json_TB.encode("utf-8"))

# Envia los datos
socket_Bob.enviar(msg_cifB)
socket_Bob.enviar(mac_cifB)
socket_Bob.enviar(nonce_cifB)

###################################33
# Cerramos el socket entre B y T, no lo utilizaremos mas
socket_Bob.cerrar() 

# Paso 3) A->T: KAT(Alice, Na) en AES-GCM
#########################################

# (A realizar por el alumno/a...)

# Crear el socket de escucha de Alice (5551)
print("Esperando a Alice...")
socket_Alice = SOCKET_SIMPLE_TCP('127.0.0.1', 5551)
socket_Alice.escuchar()

# Recibe el mensaje
cif = socket_Alice.recibir()
cif_mac = socket_Alice.recibir()
cif_nonce = socket_Alice.recibir()

# Descifro los datos con AES GCM
datos_descifrado_AT = funciones_aes.descifrarAES_GCM(KAT, cif_nonce, cif, cif_mac)

# Decodifica el contenido: Bob, Nb
json_AT = datos_descifrado_AT.decode("utf-8" ,"ignore")
print("A -> T (descifrado): " + json_AT)
msg_AT = json.loads(json_AT)

# Extraigo el contenido
t_alice, t_na = msg_AT
t_na = bytearray.fromhex(t_na)

# Paso 4) T->A: KAT(K1, K2, Na) en AES-GCM
##########################################
# Creo el mensaje con las claves y el nonce de B
msg_TA = []
msg_TA.append(K1.hex())
msg_TA.append(K2.hex())
msg_TA.append(t_na.hex())
json_TA = json.dumps(msg_TA)
print("T -> A (cifrado): " + json_TA)

# Cifro en mensaje
aes_cifA = funciones_aes.iniciarAES_GCM(KAT)
msg_cifA, mac_cifA, nonce_cifA = funciones_aes.cifrarAES_GCM(aes_cifA, json_TA.encode("utf-8"))

# Envia los datos
socket_Alice.enviar(msg_cifA)
socket_Alice.enviar(mac_cifA)
socket_Alice.enviar(nonce_cifA)

# Cerramos el socket entre B y T, no lo utilizaremos mas
socket_Alice.cerrar() 
# (A realizar por el alumno/a...)
