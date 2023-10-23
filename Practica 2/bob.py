import funciones_rsa as r
import socket_class as s
import funciones_aes as a

# APARTADO 1
# cargar claves
BKpriv = r.cargar_RSAKey_Privada("BPriv.txt","123456")
AKpub = r.cargar_RSAKey_Publica("APub.txt")

# recibir texto
socketclient = s.SOCKET_SIMPLE_TCP('127.0.0.1', 5551)
socketclient.escuchar()
textoCifrado = socketclient.recibir()
firma = socketclient.recibir()

# descifrar texto
textoDescifrado = r.descifrarRSA_OAEP(textoCifrado, BKpriv)
print(textoDescifrado)
valido = r.comprobarRSA_PSS(textoDescifrado, firma, AKpub)
print(valido)

# APARTADO 2
cadena = "Hola Alice"
(aesCifrado, nonce) = a.iniciarAES_CTR_cifrado(textoDescifrado)
cadenaCifrada = a.cifrarAES_CTR(aesCifrado, cadena.encode("utf-8"))
firmaCadena = r.firmarRSA_PSS(cadena.encode("utf-8"), BKpriv)

socketclient.enviar(nonce)
socketclient.enviar(cadenaCifrada)
socketclient.enviar(firmaCadena)

nonceA = socketclient.recibir()
cadenaCifradaA = socketclient.recibir()
hashFirmadoA = socketclient.recibir()
aesDescifradoA = a.iniciarAES_CTR_descifrado(textoDescifrado, nonceA)
textoClaroA = a.descifrarAES_CTR(aesDescifradoA, cadenaCifradaA)
firmaA = r.comprobarRSA_PSS(textoClaroA,hashFirmadoA,AKpub)
print(f"Cadena recibida: {textoClaroA} Validez: {firmaA}")
socketclient.cerrar()