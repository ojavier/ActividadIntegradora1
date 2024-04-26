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
        return False, -1  # Cambio aquí, devolvemos False y -1 si no se encuentra el patrón
    
    long = calcular_longitud(pat)  # Calcula Longitud para el patrón
    i = 0
    j = 0
    while i < N:
        if j < M and pat[j] == txt[i]:
            i += 1
            j += 1
        if j == M:
            return True, i - j  # Cambio aquí, devolvemos True y la posición donde se encontró el patrón
            j = long[j-1]  # Ajusta j basado en la longitud previamente calculada
        elif i < N and pat[j] != txt[i]:
            if j != 0:
                j = long[j-1]  
            else:
                i += 1
    return False, -1  # Cambio aquí, devolvemos False y -1 si no se encuentra el patrón


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
                found, pos = kmp_search(mcode_contenido_hex, transmission_contenido_hex[inicio:])
                if found:
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

def longest_common_substring(txt1, txt2):
    m = len(txt1)
    n = len(txt2)
    longest = 0
    end_pos = 0
    lookup = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if txt1[i - 1] == txt2[j - 1]:
                lookup[i][j] = lookup[i - 1][j - 1] + 1
                if lookup[i][j] > longest:
                    longest = lookup[i][j]
                    end_pos = i
    return end_pos - longest + 1, end_pos

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
    # Búsqueda del substring más largo común
    for mcode_archivo in mcode_archivos:
        mcode = leer_archivo(mcode_archivo)
        for transmission_archivo in transmission_archivos:
            transmission = leer_archivo(transmission_archivo)
            found, pos = kmp_search(mcode, transmission)
            if found:
                print("True", end=" ")
                print(pos + 1)  # Corrección aquí, sumamos 1 a pos para obtener la posición correcta

    for transmission_archivo in transmission_archivos:
        transmission = leer_archivo(transmission_archivo)
        transmission1 = leer_archivo(transmission_archivos[0])
        start, end = longest_common_substring(transmission1, transmission)
        print(start, end, end=" ")

    transmission1 = leer_archivo(transmission_archivos[0])
    transmission2 = leer_archivo(transmission_archivos[1])
    start, end = longest_common_substring(transmission1, transmission2)
    print(start, end)


if __name__ == "__main__":
    main()