# Función para leer el contenido de un archivo de texto
def leer_archivo(nombre_archivo):
    with open(nombre_archivo, 'r') as archivo:
        contenido = archivo.read()
    return contenido

# Función para encontrar el palíndromo más largo en una cadena
def encontrar_palindromo(cadena):
    longest_palindrome = ''
    for i in range(len(cadena)):
        for j in range(i+1, len(cadena) + 1):
            substring = cadena[i:j]
            if substring == substring[::-1] and len(substring) > len(longest_palindrome):
                longest_palindrome = substring
    return longest_palindrome


# Archivos de transmisión
transmission1 = leer_archivo("transmission01.txt")
transmission2 = leer_archivo("transmission02.txt")

# Archivos de mcode
mcode1 = leer_archivo("mcode01.txt")
mcode2 = leer_archivo("mcode02.txt")
mcode3 = leer_archivo("mcode03.txt")

# Buscar palíndromos en los archivos de transmisión
for transmission, i in zip([transmission1, transmission2], [1, 2]):
    palindrome = encontrar_palindromo(transmission)
    start = transmission.find(palindrome) + 1
    end = start + len(palindrome) - 1
    print(start, end, end=" ")
