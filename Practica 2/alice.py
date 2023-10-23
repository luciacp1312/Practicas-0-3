import funciones_rsa as r
import socket_class as s
import funciones_aes as a

# APARTADO 1
# cargar claves
AKpriv = r.cargar_RSAKey_Privada("APriv.txt","123456")
BKpub = r.cargar_RSAKey_Publica("BPub.txt")

# cifrar
K1 = a.crear_AESKey()
cifrado = r.cifrarRSA_OAEP(K1, BKpub)
firmado = r.firmarRSA_PSS(K1, AKpriv)

#Enviar con sockets
socketclient = s.SOCKET_SIMPLE_TCP('127.0.0.1', 5551)
socketclient.conectar()
socketclient.enviar(cifrado)
socketclient.enviar(firmado)

# APARTADO 2
nonceBob = socketclient.recibir()
cadenaBob = socketclient.recibir()
hashFirmadoBob = socketclient.recibir()
descifradoBob = a.iniciarAES_CTR_descifrado(K1,nonceBob)
textoClaroBob = a.descifrarAES_CTR(descifradoBob, cadenaBob)
firmaBob = r.comprobarRSA_PSS(textoClaroBob, hashFirmadoBob, BKpub)
print(f"Cadena recibida: {textoClaroBob} Validez: {firmaBob}")


cadena = "Hola Bob"
(aesCifrado, nonce) = a.iniciarAES_CTR_cifrado(K1)
cadenaCifrada = a.cifrarAES_CTR(aesCifrado, cadena.encode("utf-8"))
firmaCadena = r.firmarRSA_PSS(cadena.encode("utf-8"), AKpriv)

socketclient.enviar(nonce)
socketclient.enviar(cadenaCifrada)
socketclient.enviar(firmaCadena)
socketclient.cerrar()