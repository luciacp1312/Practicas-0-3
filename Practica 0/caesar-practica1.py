# Apartado a
def cifradoCesarAlfabetoInglesMAY(cadena):
    """
    Devuelve un cifrado Cesar tradicional (+3)
    """
    # Definir la nueva cadena resultado
    resultado = ''
    # Realizar el "cifrado", sabiendo que A = 65, Z = 90, a = 97, z = 122
    i = 0
    while i < len(cadena):
        # Recoge el caracter a cifrar
        ordenClaro = ord(cadena[i])
        #ordenCifrado = 0 No es necesario inicializarlo aqui, ya que lo hara dentro del if
        # Cambia el caracter a cifrar
        if (ordenClaro >= 65 and ordenClaro <= 90):
			# ==COMPLETAR para guardar en ordenCifrado el cifrado de ordenClaro==
            ordenCifrado = (((ordenClaro - 65) + 3) % 26) + 65
            resultado = resultado + chr(ordenCifrado)
        # Añade el caracter cifrado al resultado
        i = i + 1
    # devuelve el resultado
    return resultado

claroCESARMAY = 'VENI VIDI VINCI AURIA'
print(claroCESARMAY)
cifradoCESARMAY = cifradoCesarAlfabetoInglesMAY(claroCESARMAY) 
print(cifradoCESARMAY)

# Apartado b
def descifradoCesarAlfabetoInglesMAY(cadena):
    """
    Devuelve un descifrado Cesar tradicional (-3)
    """
    # Definir la nueva cadena resultado
    resultado = ''
    # Realizar el "cifrado", sabiendo que A = 65, Z = 90, a = 97, z = 122
    i = 0
    while i < len(cadena):
        # Recoge el caracter a cifrar
        ordenCifrado = ord(cadena[i])
        #ordenCifrado = 0 No es necesario inicializarlo aqui, ya que lo hara dentro del if
        # Cambia el caracter a cifrar
        if (ordenCifrado >= 65 and ordenCifrado <= 90):
			# ==COMPLETAR para guardar en ordenClaro el descifrado de ordenCifrado==
            ordenClaro = (((ordenCifrado - 65) - 3) % 26) + 65
            resultado = resultado + chr(ordenClaro)
        # Añade el caracter cifrado al resultado
        i = i + 1
    # devuelve el resultado
    return resultado

descifradoCESARMAY = descifradoCesarAlfabetoInglesMAY(cifradoCESARMAY)
print(descifradoCESARMAY)


# Apartado c
def cifradoCesarAlfabetoInglesMAYi(cadena, i):
    """
    Devuelve un cifrado Cesar variable i
    """
    # Definir la nueva cadena resultado
    resultado = ''
    # Realizar el "cifrado", sabiendo que A = 65, Z = 90, a = 97, z = 122
    cont = 0
    while cont < len(cadena):
        # Recoge el caracter a cifrar
        ordenClaro = ord(cadena[cont])
        #ordenCifrado = 0 No es necesario inicializarlo aqui, ya que lo hara dentro del if
        # Cambia el caracter a cifrar
        if (ordenClaro >= 65 and ordenClaro <= 90):
			# ==COMPLETAR para guardar en ordenCifrado el cifrado de ordenClaro==
            ordenCifrado = (((ordenClaro - 65) + i) % 26) + 65
            resultado = resultado + chr(ordenCifrado)
        # Añade el caracter cifrado al resultado
        cont = cont + 1
    # devuelve el resultado
    return resultado

claroCESARMAY = 'VENI VIDI VINCI AURIA'
print("Cifrado i en claro " + claroCESARMAY)
cifradoCESARMAY = cifradoCesarAlfabetoInglesMAYi(claroCESARMAY, 2) 
print("Cifrado i cifrado " + cifradoCESARMAY)


def descifradoCesarAlfabetoInglesMAYi(cadena, i):
    """
    Devuelve un descifrado Cesar tradicional (-i)
    """
    # Definir la nueva cadena resultado
    resultado = ''
    # Realizar el "cifrado", sabiendo que A = 65, Z = 90, a = 97, z = 122
    cont = 0
    while cont < len(cadena):
        # Recoge el caracter a cifrar
        ordenCifrado = ord(cadena[cont])
        #ordenCifrado = 0 No es necesario inicializarlo aqui, ya que lo hara dentro del if
        # Cambia el caracter a cifrar
        if (ordenCifrado >= 65 and ordenCifrado <= 90):
			# ==COMPLETAR para guardar en ordenClaro el descifrado de ordenCifrado==
            ordenClaro = (((ordenCifrado - 65) - i) % 26) + 65
            resultado = resultado + chr(ordenClaro)
        # Añade el caracter cifrado al resultado
        cont = cont + 1
    # devuelve el resultado
    return resultado


descifradoCESARMAY = descifradoCesarAlfabetoInglesMAYi(cifradoCESARMAY, 2)
print("Desifrado i en claro " + descifradoCESARMAY)

# Apartado d
def cifradoCesarAlfabetoInglesMAYiSim(cadena, i):
    """
    Devuelve un cifrado Cesar variable i
    """
    # Definir la nueva cadena resultado
    resultado = ''
    # Realizar el "cifrado", sabiendo que A = 65, Z = 90, a = 97, z = 122
    cont = 0
    while cont < len(cadena):
        # Recoge el caracter a cifrar
        ordenClaro = ord(cadena[cont])
        #ordenCifrado = 0 No es necesario inicializarlo aqui, ya que lo hara dentro del if
        # Cambia el caracter a cifrar
        if (ordenClaro >= 65 and ordenClaro <= 90):
			# ==COMPLETAR para guardar en ordenCifrado el cifrado de ordenClaro==
            ordenCifrado = (((ordenClaro - 65) + i) % 26) + 65
            resultado = resultado + chr(ordenCifrado)
        # Detecta otros símbolos
        else:
            ordenCifrado = (ordenClaro + i) % 127
            resultado = resultado + chr(ordenCifrado)
        # Añade el caracter cifrado al resultado
        cont = cont + 1
    # devuelve el resultado
    return resultado

claroCESARMAY = 'VENI VIDI VINCI AURIAab!4345'
print("Cifrado i simbolos en claro " + claroCESARMAY)
cifradoCESARMAY = cifradoCesarAlfabetoInglesMAYiSim(claroCESARMAY, 2) 
print("Cifrado i simbolos cifrado " + cifradoCESARMAY)


def descifradoCesarAlfabetoInglesMAYiSim(cadena, i):
    """
    Devuelve un descifrado Cesar tradicional (-i)
    """
    # Definir la nueva cadena resultado
    resultado = ''
    # Realizar el "cifrado", sabiendo que A = 65, Z = 90, a = 97, z = 122
    cont = 0
    while cont < len(cadena):
        # Recoge el caracter a cifrar
        ordenCifrado = ord(cadena[cont])
        #ordenCifrado = 0 No es necesario inicializarlo aqui, ya que lo hara dentro del if
        # Cambia el caracter a cifrar
        if (ordenCifrado >= 65 and ordenCifrado <= 90):
			# ==COMPLETAR para guardar en ordenClaro el descifrado de ordenCifrado==
            ordenClaro = (((ordenCifrado - 65) - i) % 26) + 65
            resultado = resultado + chr(ordenClaro)
        # Detecta otros símbolos
        else:
            ordenClaro = ((ordenCifrado - i)) % 127
            resultado = resultado + chr(ordenClaro)
        # Añade el caracter cifrado al resultado
        cont = cont + 1
    # devuelve el resultado
    return resultado


descifradoCESARMAY = descifradoCesarAlfabetoInglesMAYiSim(cifradoCESARMAY, 2)
print("Desifrado i simbolos en claro " + descifradoCESARMAY)