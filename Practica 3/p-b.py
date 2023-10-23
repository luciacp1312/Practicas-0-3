from Crypto.Hash import SHA256, HMAC
import base64
import json
import sys
from socket_class import SOCKET_SIMPLE_TCP
import funciones_aes
from Crypto.Random import get_random_bytes

# Paso 0: Inicializacion
########################

# Lee clave KBT
KBT = open("KBT.bin", "rb").read()

# Paso 1) B->T: KBT(Bob, Nb) en AES-GCM
#######################################

# Crear el socket de conexion con T (5551)
print("Creando conexion con T...")
socket = SOCKET_SIMPLE_TCP('127.0.0.1', 5551)
socket.conectar()

# Crea los campos del mensaje
t_n_origen = get_random_bytes(16) ## Para el nonce de B

# Codifica el contenido (los campos binarios en una cadena) y contruyo el mensaje JSON
msg_TE = []
msg_TE.append("Bob")
msg_TE.append(t_n_origen.hex())
json_ET = json.dumps(msg_TE) # serializa/convierte un objeto de python en cadena JSON
print("B -> T (cifrado): " + json_ET)

# Cifra los datos con AES GCM
aes_engine = funciones_aes.iniciarAES_GCM(KBT)
cifrado, cifrado_mac, cifrado_nonce = funciones_aes.cifrarAES_GCM(aes_engine,json_ET.encode("utf-8")) # encode sirve para convertir una cadena de texto en formato JSON a una secuencia de bytes

# Envia los datos
socket.enviar(cifrado)
socket.enviar(cifrado_mac)
socket.enviar(cifrado_nonce)

# Paso 2) T->B: KBT(K1, K2, Nb) en AES-GCM
##########################################

# (A realizar por el alumno/a...)
cifradoB = socket.recibir()
macB = socket.recibir()
nonceB = socket.recibir()

# Descifro los datos con AES GCM
datos_descifrado_BT = funciones_aes.descifrarAES_GCM(KBT, nonceB, cifradoB, macB)

# Decodifica el contenido: Bob, Nb
json_BT = datos_descifrado_BT.decode("utf-8" ,"ignore")
print("B -> T (descifrado): " + json_BT)
msg_BT = json.loads(json_BT) # Parsea json_BT y convierte el json en un objeto de python

# Extraigo el contenido
K1, K2, t_nb = msg_BT
K1 = bytearray.fromhex(K1) # necesario pasarlo a bytearray para trabajar con binarios
K2 = bytearray.fromhex(K2)
t_nb = bytearray.fromhex(t_nb)

if(t_nb == t_n_origen):
    print("Mismo nonce")
else:
    print("Nonce distinto")
    exit
# Cerramos el socket entre B y T, no lo utilizaremos mas
socket.cerrar()

# Paso 5) A->B: KAB(Nombre) en AES-CTR (confidencialidad) con HMAC (autenticidad e integridad)
###############################################

# (A realizar por el alumno/a...)
# Crear el socket de conexion con T (5553)
print("Esperando a Alice...")
socket = SOCKET_SIMPLE_TCP('127.0.0.1', 5553) # usamos otro ya que se va a usar para un tipo de comunicación distinta
socket.escuchar()

paquete = socket.recibir()
# Decodifica el contenido
json_AB = paquete.decode("utf-8", "ignore")
print("A -> B (descifrado): " + json_AB)
msg_AB = json.loads(json_AB)

# Extraigo el contenido
cifradoAB, nonceAB, macAB = msg_AB # El mac de por si es una secuencia de bytes, por lo que no uso bytearray
cifradoAB = bytearray.fromhex(cifradoAB)
nonceAB = bytearray.fromhex(nonceAB)
# Descifro los datos con CTR
aes_descif = funciones_aes.iniciarAES_CTR_descifrado(K1, nonceAB)
datos_descifrado_AB = funciones_aes.descifrarAES_CTR(aes_descif,cifradoAB)
msgClaro_AB = datos_descifrado_AB.decode("utf-8")
print("A -> B (descifrado): " + msgClaro_AB)

# Calculo MAC
macCalcB = HMAC.new(K2,digestmod=SHA256)
macCalcB.update(msgClaro_AB.encode("utf-8"))
# macCalcB = HMAC.new(K2, msg=msgClaro_AB.encode("utf-8"), digestmod=SHA256)    Tambien asi

try:
    macCalcB.hexverify(macAB) # calcula internamente el MAC, al igual que cuando hacemos .digest()
    print("Mensaje correcto")
except ValueError:
    print("Mensaje modificado")
    socket.cerrar()
    exit()

# Paso 6) B->A: KAB(Apellido) en AES-CTR con HMAC
#################################################

# (A realizar por el alumno/a...)
# Codifica el contenido (los campos binarios en una cadena) y contruyo el mensaje JSON
apellido = "Martinez"

# Cifra los datos con AES GCM
aes_cif, nonce_ini = funciones_aes.iniciarAES_CTR_cifrado(K1)
cifradoAB = funciones_aes.cifrarAES_CTR(aes_cif, apellido.encode("utf-8"))

# Creo MAC
hsendAB = HMAC.new(K2, msg=apellido.encode("utf-8"), digestmod=SHA256)
macAB = hsendAB.digest()

# Crea el mensaje y envia los datos
msg_AB = []
msg_AB.append(cifradoAB.hex())
msg_AB.append(nonce_ini.hex())
msg_AB.append(macAB.hex())
json_AB = json.dumps(msg_AB)
socket.enviar(json_AB.encode("utf-8"))

#socket.cerrar()
# Paso 7) A->B: KAB(END) en AES-CTR con HMAC
############################################

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
macCalcB = HMAC.new(K2,digestmod=SHA256)
macCalcB.update(msgClaro_AB.encode("utf-8"))

try:
    macCalcB.hexverify(macAB)
    print("Mensaje correcto")
except ValueError:
    print("Mensaje modificado")
    socket.cerrar()
    exit()
    
print("Se cierra la conexion")
socket.cerrar()
