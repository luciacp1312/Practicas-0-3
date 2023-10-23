
from Crypto.Hash import SHA256, HMAC
import base64
import json
import sys
from socket_class import SOCKET_SIMPLE_TCP
import funciones_aes
from Crypto.Random import get_random_bytes

# Paso 0: Inicializacion
########################

# (A realizar por el alumno/a...)
KAT = open("KAT.bin", "rb").read()

# Paso 3) A->T: KAT(Alice, Na) en AES-GCM
#########################################
# (A realizar por el alumno/a...)

# Crear el socket de conexion con T (5551)
print("Creando conexion con T...")
socket = SOCKET_SIMPLE_TCP('127.0.0.1', 5551)
socket.conectar()

# Crea los campos del mensaje
t_n_origen = get_random_bytes(16) ## Para el nonce de B

# Codifica el contenido (los campos binarios en una cadena) y contruyo el mensaje JSON
msg_TE = []
msg_TE.append("Alice")
msg_TE.append(t_n_origen.hex())
json_ET = json.dumps(msg_TE)
print("A -> T (cifrado): " + json_ET)

# Cifra los datos con AES GCM
aes_engine = funciones_aes.iniciarAES_GCM(KAT)
cifrado, cifrado_mac, cifrado_nonce = funciones_aes.cifrarAES_GCM(aes_engine,json_ET.encode("utf-8"))

# Envia los datos
socket.enviar(cifrado)
socket.enviar(cifrado_mac)
socket.enviar(cifrado_nonce)


# Paso 4) T->A: KAT(K1, K2, Na) en AES-GCM
##########################################

# (A realizar por el alumno/a...)
# A recibe datos
cifradoA = socket.recibir()
macA = socket.recibir()
nonceA = socket.recibir()
# Descifrar mensaje
datos_descifrado_AT = funciones_aes.descifrarAES_GCM(KAT, nonceA, cifradoA, macA)
# Decodifica el contenido
json_AT = datos_descifrado_AT.decode("utf-8" ,"ignore")
print("A -> T (descifrado): " + json_AT)
msg_AT = json.loads(json_AT)

K1, K2, t_na = msg_AT

K1 = bytearray.fromhex(K1)
K2 = bytearray.fromhex(K2)
t_na = bytearray.fromhex(t_na)

if(t_na == t_n_origen):
    print("Mismo nonce")
else:
    print("Distinto nonce")
    exit

socket.cerrar()
# Paso 5) A->B: KAB(Nombre) en AES-CTR con HMAC
###############################################

# (A realizar por el alumno/a...)

# Crear el socket de conexion con T (5553)
print("Creando conexion con Bob...")
socket = SOCKET_SIMPLE_TCP('127.0.0.1', 5553)
socket.conectar()

# Codifica el contenido (los campos binarios en una cadena) y contruyo el mensaje JSON
'''msg_AB = []
msg_AB.append("Juan")
json_AB = json.dumps(msg_AB)'''
nombre = "Juan"

# Cifra los datos con AES GCM
aes_cif, nonce_ini = funciones_aes.iniciarAES_CTR_cifrado(K1)
cifradoAB = funciones_aes.cifrarAES_CTR(aes_cif, nombre.encode("utf-8"))

# Creo MAC
hsendAB = HMAC.new(K2, msg=nombre.encode("utf-8"), digestmod=SHA256)
macAB = hsendAB.digest()

# Crea el mensaje y envia los datos
msg_AB = []
msg_AB.append(cifradoAB.hex())
msg_AB.append(nonce_ini.hex())
msg_AB.append(macAB.hex())
json_AB = json.dumps(msg_AB)
socket.enviar(json_AB.encode("utf-8"))

#socket.cerrar()

# Paso 6) B->A: KAB(Apellido) en AES-CTR con HMAC
#################################################

# (A realizar por el alumno/a...)
paquete = socket.recibir()
# Decodifica el contenido
json_AB = paquete.decode("utf-8", "ignore")
print("A -> B (descifrado): " + json_AB)
msg_AB = json.loads(json_AB)

# Extraigo el contenido
cifradoAB, nonceAB, macAB = msg_AB
cifradoAB = bytearray.fromhex(cifradoAB)
nonceAB = bytearray.fromhex(nonceAB)
# Descifro los datos con CTR
aes_descif = funciones_aes.iniciarAES_CTR_descifrado(K1, nonceAB)
datos_descifrado_AB = funciones_aes.descifrarAES_CTR(aes_descif,cifradoAB)
msgClaro_AB = datos_descifrado_AB.decode("utf-8")
print("A -> B (descifrado): " + msgClaro_AB)

# Calculo MAC
macCalcA = HMAC.new(K2,digestmod=SHA256)
macCalcA.update(msgClaro_AB.encode("utf-8"))

try:
    macCalcA.hexverify(macAB)
    print("Mensaje correcto")
except ValueError:
    print("Mensaje modificado")
    socket.cerrar()
    exit()
    
# Paso 7) A->B: KAB(END) en AES-CTR con HMAC
############################################

# (A realizar por el alumno/a...)
# Codifica el contenido (los campos binarios en una cadena) y contruyo el mensaje JSON
end = "END"

# Cifra los datos con AES GCM
aes_cif, nonce_ini = funciones_aes.iniciarAES_CTR_cifrado(K1)
cifradoAB = funciones_aes.cifrarAES_CTR(aes_cif, end.encode("utf-8"))

# Creo MAC
hsendAB = HMAC.new(K2, msg=end.encode("utf-8"), digestmod=SHA256)
macAB = hsendAB.digest()

# Crea el mensaje y envia los datos
msg_AB = []
msg_AB.append(cifradoAB.hex())
msg_AB.append(nonce_ini.hex())
msg_AB.append(macAB.hex())
json_AB = json.dumps(msg_AB)
socket.enviar(json_AB.encode("utf-8"))

socket.cerrar()
