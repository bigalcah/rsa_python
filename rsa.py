import random
from sympy import isprime, mod_inverse

# Función para generar un número primo grande
def generar_primo(bits):
    while True:
        primo = random.getrandbits(bits)
        if isprime(primo):
            return primo
        
def cambioBase(num, base):
    resultado = []
    while (num > 0):
        residuo = num % base
        resultado.append(residuo)
        num = num // base
    resultado = resultado[::-1]
    numero_str = ''.join(str(d) for d in resultado)
    return numero_str

# Algoritmo Square and Multiply para la exponentiación modular rápida
def square_and_multiply(base, exponente, modulo):
    resultado = 1
    binario = cambioBase(exponente, 2)  # Conversión a binario
    for bit in binario:
        resultado = (resultado * resultado) % modulo
        if bit == '1':
            resultado = (resultado * base) % modulo
    return resultado

# Generación de claves RSA
def generar_claves(bits=1024):
    p = generar_primo(bits)
    q = generar_primo(bits)
    n = p * q
    phi_n = (p - 1) * (q - 1)

    # Selecciona e tal que sea coprimo con phi_n
    e = 65537  # Valor comúnmente usado para e
    d = mod_inverse(e, phi_n)
    return (e, n), (d, n), p, q

# Cifrado RSA
def cifrar(mensaje, clave_publica, n):
    e, n = clave_publica
    # Convertir el mensaje a un número
    m = int.from_bytes(mensaje.encode('utf-8'), 'big')
    # Cifrado usando Square and Multiply
    c = square_and_multiply(m, e, n)
    return c

# Descifrado RSA optimizado con CRT
def descifrar(cifrado, clave_privada, n, p, q):
    d, n = clave_privada
    # Descifrado optimizado con CRT
    dp = d % (p - 1)
    dq = d % (q - 1)
    qinv = mod_inverse(q, p)
    
    # Cálculos separados
    m1 = square_and_multiply(cifrado, dp, p)
    m2 = square_and_multiply(cifrado, dq, q)

    # Combinación usando el CRT
    h = (qinv * (m1 - m2)) % p
    m = m2 + h * q
    # Convertir de número a texto
    mensaje = m.to_bytes((m.bit_length() + 7) // 8, 'big').decode('utf-8', errors='ignore')
    return mensaje

# Prueba del programa
def main():
    # Generar claves
    clave_publica, clave_privada, p, q = generar_claves(bits=1024)
    
    # Mensaje a cifrar
    mensaje = "Hola, este es un mensaje cifrado con RSA optimizado."
    print(f"Mensaje original: {mensaje}")
    
    # Cifrar
    cifrado = cifrar(mensaje, clave_publica, clave_publica[1])
    print(f"Texto cifrado: {cifrado}")

    # Descifrar
    descifrado = descifrar(cifrado, clave_privada, clave_privada[1], p, q)
    print(f"Mensaje descifrado: {descifrado}")

if __name__ == "__main__":
    main()
