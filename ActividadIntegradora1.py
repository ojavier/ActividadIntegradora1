import os

# Función para leer el contenido de un archivo de texto
def leer_archivo(nombre_archivo):
    with open(nombre_archivo, 'r') as archivo:
        contenido = archivo.read().replace('\n', '')
    return contenido

# Función para calcular la longitud de la subcadena prefijo/sufijo (LPS)
def calcular_longitud(pat):
    M = len(pat)
    long = [0]*M  # Inicializa una lista para almacenar la longitud
    len_ = 0
    i = 1
    while i < M:
        if pat[i] == pat[len_]:
            len_ += 1 
            long[i] = len_  # Almacena la longitud para la posición actual
            i += 1
        else:
            if len_ != 0:
                len_ = long[len_-1]  # Ajusta len_ a la longitud calculada
            else:
                long[i] = 0  # Si no existe para la posición actual, establece la longitud como 0
                i += 1
    return long

# Búsqueda de patrones utilizando el algoritmo de Knuth-Morris-Pratt (KMP)
def kmp_search(pat, txt):
    M = len(pat)
    N = len(txt)
    if M == 0 or N == 0:
        return -1
    
    long = calcular_longitud(pat)  # Calcula Longitud para el patrón
    i = 0
    j = 0
    while i < N:
        if j < M and pat[j] == txt[i]:
            i += 1
            j += 1
        if j == M:
            return i-j  # Devuelve la posición donde se encontró el patrón en el archivo transmission
            j = long[j-1]  # Ajusta j basado en la longitud previamente calculada
        elif i < N and pat[j] != txt[i]:
            if j != 0:
                j = long[j-1]  
            else:
                i += 1
    return -1

# Función para encontrar el palíndromo más largo en una cadena
def encontrar_palindromo(cadena):
    longest_palindrome = ''
    for i in range(len(cadena)):
        for j in range(i+1, len(cadena) + 1):
            substring = cadena[i:j]
            if substring == substring[::-1] and len(substring) > len(longest_palindrome):
                longest_palindrome = substring
    return longest_palindrome

# Función para encontrar el código de mcode en los archivos de transmission
def encontrar_codigo_transmision(mcode_archivos, transmission_archivos):
    for mcode_archivo in mcode_archivos:
        mcode_contenido_hex = leer_archivo(mcode_archivo)
        for i, transmission_archivo in enumerate(transmission_archivos, start=1):
            transmission_contenido_hex = leer_archivo(transmission_archivo)
            posiciones = []
            inicio = 0
            while True:
                pos = kmp_search(mcode_contenido_hex, transmission_contenido_hex[inicio:])
                if pos != -1:
                    inicio += pos + 1
                    fin = inicio + len(mcode_contenido_hex)
                    posiciones.append((inicio, fin))
                else:
                    break
            if posiciones:
                print("true", end=": ")
                for inicio, fin in posiciones:
                    print(f"({inicio}, {fin})", end=" ")
            else:
                print("false", end=" ")
        print()

class SuffixTree:
    def __init__(self, cadena):
        self.cadena = cadena
        self.raiz = {}
        self._construir_arbol()

    def _agregar_sufijo(self, sufijo, pos):
        nodo_actual = self.raiz
        for char in sufijo:
            if char not in nodo_actual:
                nodo_actual[char] = {}
            nodo_actual = nodo_actual[char]
        nodo_actual['pos'] = pos

    def _construir_arbol(self):
        n = len(self.cadena)
        for i in range(n):
            self._agregar_sufijo(self.cadena[i:], i)

    def buscar_subcadena(self, subcadena):
        nodo_actual = self.raiz
        for char in subcadena:
            if char in nodo_actual:
                nodo_actual = nodo_actual[char]
            else:
                return []
        return self._encontrar_posiciones(nodo_actual)

    def _encontrar_posiciones(self, nodo):
        if 'pos' in nodo:
            return [nodo['pos']]
        posiciones = []
        for hijo in nodo.values():
            posiciones.extend(self._encontrar_posiciones(hijo))
        return posiciones

# Función para encontrar todas las ocurrencias del substring más largo común entre archivos de transmisión
def encontrar_todas_ocurrencias_substring_comun_archivos(transmission_archivo1, transmission_archivo2):
    transmission_contenido1 = leer_archivo(transmission_archivo1)
    transmission_contenido2 = leer_archivo(transmission_archivo2)
    sufijo1 = SuffixTree(transmission_contenido1)
    sufijo2 = SuffixTree(transmission_contenido2)
    
    ocurrencias1 = []
    ocurrencias2 = []
    
    for i in range(len(transmission_contenido1)):
        for j in range(i + 1, len(transmission_contenido1) + 1):
            subcadena = transmission_contenido1[i:j]
            posiciones = sufijo2.buscar_subcadena(subcadena)
            if posiciones:
                ocurrencias1.append((i + 1, j))
    
    for i in range(len(transmission_contenido2)):
        for j in range(i + 1, len(transmission_contenido2) + 1):
            subcadena = transmission_contenido2[i:j]
            posiciones = sufijo1.buscar_subcadena(subcadena)
            if posiciones:
                ocurrencias2.append((i + 1, j))
    
    return max(ocurrencias1, key=lambda x: x[1] - x[0]), max(ocurrencias2, key=lambda x: x[1] - x[0])


def main():
    mcode_archivos = ["mcode01.txt", "mcode02.txt", "mcode03.txt"]
    transmission_archivos = ["transmission01.txt", "transmission02.txt"]

    # Parte 1
    print("~~~~~~~~~~~ PARTE 1 ~~~~~~~~~~~")
    encontrar_codigo_transmision(mcode_archivos, transmission_archivos)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

    # Parte 2
    print("~~~~~~~~~~~ PARTE 2 ~~~~~~~~~~~")
    for transmission_archivo in transmission_archivos:
        transmission_contenido = leer_archivo(transmission_archivo)
        start = transmission_contenido.find(encontrar_palindromo(transmission_contenido)) + 1
        end = start + len(encontrar_palindromo(transmission_contenido)) - 1
        print(f"({start}, {end})", end=" ")
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

    # Parte 3
    print("~~~~~~~~~~~ PARTE 3 ~~~~~~~~~~~")
    for i in range(len(transmission_archivos)):
        for j in range(i + 1, len(transmission_archivos)):
            ocurrencias1, ocurrencias2 = encontrar_todas_ocurrencias_substring_comun_archivos(transmission_archivos[i], transmission_archivos[j])
            print(f"Archivo {i+1} y Archivo {j+1} (primer archivo -> segundo archivo):")
            for inicio, fin in ocurrencias1:
                print(f"({inicio}, {fin})")
            print(f"Archivo {j+1} y Archivo {i+1} (segundo archivo -> primer archivo):")
            for inicio, fin in ocurrencias2:
                print(f"({inicio}, {fin})")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")


if __name__ == "__main__":
    main()
