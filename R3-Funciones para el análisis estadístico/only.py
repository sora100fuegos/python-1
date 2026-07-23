# Se importa librería numpy
import numpy as np

# Generar un arreglo de 1000 números con media 5 y desviación estándar 2

np.random.seed(42)
listaNumeros = np.random.normal(loc=5, scale=2, size=1000)

# Función para obtener promedio
def obtener_promedio(datos):
    return np.mean(datos)

# Función para obtener mediana
def obtener_mediana(datos):
    return np.median(datos)

# Función para obtener cuartiles
def obtener_cuartiles(datos):
    return {
        "Q1": np.percentile(datos, 25),
        "Q2": np.percentile(datos, 50),  # mediana
        "Q3": np.percentile(datos, 75)
    }

# Función para obtener deciles
def obtener_deciles(datos):
    deciles = {}
    for i in range(1, 10):
        deciles[f"D{i}"] = np.percentile(datos, i * 10)
    return deciles

# Función para obtener cualquier percentil
def obtener_percentil(datos, percentil):
    return np.percentile(datos, percentil)

# Función para obtener percentiles extremos
def obtener_percentiles_extremos(datos):
    return {
        "extremo_inferior_p2": np.percentile(datos, 2),
        "extremo_superior_p98": np.percentile(datos, 98)
    }

# Ejemplos de uso
print("Promedio:", obtener_promedio(listaNumeros))
print("Mediana:", obtener_mediana(listaNumeros))
print("Cuartiles:", obtener_cuartiles(listaNumeros))
print("Deciles:", obtener_deciles(listaNumeros))
print("Percentil 35:", obtener_percentil(listaNumeros, 35))
print("Percentiles extremos:", obtener_percentiles_extremos(listaNumeros))