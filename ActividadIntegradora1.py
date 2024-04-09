import binascii

def leer_y_convertir_a_texto(nombre_archivo):
    contenido_hex = leer_archivo(nombre_archivo)
    contenido_hex = contenido_hex.strip()  # Eliminar espacios en blanco al inicio y al final
    contenido_hex = ''.join(c for c in contenido_hex if c in '0123456789abcdefABCDEF')  # Solo mantener caracteres hexadecimales
    if len(contenido_hex) % 2 != 0:
        contenido_hex = '0' + contenido_hex  # Agregar un "0" al principio si la longitud es impar
    contenido_bytes = binascii.unhexlify(contenido_hex)
    contenido_texto = contenido_bytes.decode('utf-8')  # Puedes cambiar 'utf-8' según la codificación necesaria
    return contenido_texto

# Algoritmo para la lectura de archivos
def leer_archivo(nombre_archivo):
    with open(nombre_archivo, 'r') as archivo:
        contenido = archivo.read()
    return contenido

# Ejemplos de uso
mcode1 = leer_y_convertir_a_texto("mcode01.txt")
mcode2 = leer_y_convertir_a_texto("mcode02.txt")
mcode3 = leer_y_convertir_a_texto("mcode03.txt")

transmission1 = leer_y_convertir_a_texto("transmission01.txt")
transmission2 = leer_y_convertir_a_texto("transmission02.txt")


# Ejemplo de uso para imprimir el contenido del archivo "transmission01.txt" en texto plano
transmission1 = leer_y_convertir_a_texto("transmission02.txt")
print(transmission1)