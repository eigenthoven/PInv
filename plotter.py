import matplotlib.pyplot as plt

# Definimos varios arrays para los datos experimentales y teóricos (de solver.py)

experimental = []
solver = []

# Trasladar los datos del experimento (formato .txt) a los arrays

with open(input("Introducir nombre de archivo de experimento"), "r", encoding="utf-8") as r:
    for row in r:
        cleaned = row.strip()
        if cleaned:
            experimental.append([float(x) for x in cleaned.split()])

intervalo_tiempo = float(input("Introducir intervalo de tiempo (en segundos) empleado en el experimento: "))
