# Leer contenido de un archivo y eliminar los saltos de línea
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
                len_ = long[len_-1]  # Ajusta len_ basado en la longitud previamente calculada
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
            return i-j+1  # Devuelve la posición donde se encontró el patrón en el archivo transmission
            j = long[j-1]  # Ajusta j basado en la longitud previamente calculada
        elif i < N and pat[j] != txt[i]:
            if j != 0:
                j = long[j-1]  
            else:
                i += 1
    return -1

# Encontrar códigos de transmisión en archivos de código
def encontrar_codigo_transmision(mcode_archivos, transmission_archivos):
    for mcode_archivo in mcode_archivos:
        mcode_contenido_hex = leer_archivo(mcode_archivo)  # Lee el contenido del archivo de mcode
        for i, transmission_archivo in enumerate(transmission_archivos, start=1):
            transmission_contenido_hex = leer_archivo(transmission_archivo)  # Lee el contenido del archivo de transmisión
            pos = kmp_search(mcode_contenido_hex, transmission_contenido_hex)  # Busca el código de transmisión en el archivo de código
            if pos != -1:
                print("True", pos, end=" ")  # Imprime "True" seguido de la posición donde se encontró el código de transmisión
            else:
                print("False", end=" ")  # Imprime "False" si no se encontró el código de transmisión
        print()

def main():
    mcode_archivos = ["mcode01.txt", "mcode02.txt", "mcode03.txt"]
    transmission_archivos = ["transmission01.txt", "transmission02.txt"]

    # Parte 1
    encontrar_codigo_transmision(mcode_archivos, transmission_archivos)

if __name__ == "__main__":
    main()
