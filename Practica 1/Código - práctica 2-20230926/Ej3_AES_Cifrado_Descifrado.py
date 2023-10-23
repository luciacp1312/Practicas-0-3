from Crypto.Random import get_random_bytes
from Crypto.Cipher import DES, AES
from Crypto.Util.Padding import pad,unpad
from Crypto.Util import Counter

class AES_CIPHER_CBC:

    BLOCK_SIZE_AES = 16 # AES: Bloque de 128 bits

    def __init__(self, key):
        if len(key) != AES_CIPHER_CBC.BLOCK_SIZE_AES:
            raise ValueError("La clave debe tener 16 bytes (128 bits)")
        self.key = key

    def cifrar(self, cadena, IV):
        cipher = AES.new(self.key, AES.MODE_CBC, IV)
        ciphertext = cipher.encrypt(pad(cadena.encode("utf-8"), AES_CIPHER_CBC.BLOCK_SIZE_AES))
        return ciphertext

    def descifrar(self, cifrado, IV):
        cipher = AES.new(self.key, AES.MODE_CBC, IV)
        decrypted = unpad(cipher.decrypt(cifrado), AES_CIPHER_CBC.BLOCK_SIZE_AES)
        return decrypted.decode("utf-8")

if __name__ == "__main__":
    key = get_random_bytes(16) # Clave aleatoria de 128 bits
    IV = get_random_bytes(16)  # IV aleatorio de 128 bits
    data = "Hola Mundo con AES en modo CBC"
    aes_cipher = AES_CIPHER_CBC(key)
    cifrado = aes_cipher.cifrar(data, IV)
    descifrado = aes_cipher.descifrar(cifrado, IV)

    print("Data original:", data)
    print("Texto cifrado:", cifrado)
    print("Texto descifrado:", descifrado)