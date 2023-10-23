import funciones_rsa as r
# crear Kpub y Kpriv RSA 2048 bits de Alice
Kpriv = r.crear_RSAKey()
r.guardar_RSAKey_Publica("APub.txt",Kpriv)
r.guardar_RSAKey_Privada("APriv.txt",Kpriv, "123456")

# crear Kpub y Kpriv RSA 2048 bits de Bob
Kpriv = r.crear_RSAKey()
r.guardar_RSAKey_Publica("BPub.txt",Kpriv)
r.guardar_RSAKey_Privada("BPriv.txt",Kpriv, "123456")