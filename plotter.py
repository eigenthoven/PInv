import matplotlib.pyplot as plt
import solver_array
import math

# Definimos varios arrays para los datos experimentales y teóricos (de solver.py)

experimental = []
solver = []

# Preguuntar al usuario la introducción de los datos experimentales necesarios

n_sensor = int(input("Número de sensor (1-7): "))
dt = float(input("Intervalo de tiempo (en segundos) empleado en el experimento: "))
profundidad = float(input("Profundidad de la capa (en metros): "))
k = float(input("Conductividad térmica de la capa (en W/mK): "))
c = float(input("Calor específico de la capa (en J/kgK): "))
rho = float(input("Densidad de la capa (en kg/m3): "))
h_ext = float(input("Coeficiente de transferencia de calor externo (en W/m2K): "))
h_int = float(input("Coeficiente de transferencia de calor interno (en W/m2K): "))
t_ext = float(input("Temperatura externa (en °C): "))
t_int = experimental[0]

# Trasladar los datos del experimento (formato .txt) a los arrays

with open(input("Introducir nombre de archivo de experimento: "), "r", encoding="utf-8") as r:
    for row in r:
        cleaned = row.strip()
        if cleaned:
            experimental.append([float(x) for x in cleaned.split()])

it = len(experimental) - 1

# Estabilidad de Von Neumann

alpha = k/(c * rho) 
dn = math.sqrt((alpha * dt) / 0.25)

intervalo_tiempo = float(input("Introducir intervalo de tiempo (en segundos) empleado en el experimento: "))
solver_array.resolver_termica(dn, dt, profundidad/3, profundidad/3, profundidad/3, k, k, k, c, c, c, rho, rho, rho, h_ext, h_int, t_ext, t_int, it)
