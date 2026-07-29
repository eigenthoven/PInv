import csv
import math
import optimizador
import solver       

INTERIOR_TRANQUILO = 3.0     
EXTERIOR_SIN_VIENTO = 5.0
BRISA = 8.0
VIENTO_MODERADO = 22.0
VIENTO_FUERTE = 33.0

# Leer los datos

with open('materiales.csv', 'r') as file:
    reader = csv.DictReader(file)
    rows = list(reader)

# Creación de arrays y clasificación para los materiales según su nivel de capa

interna = []
middle = []
externa = []

for i in range(len(rows)):

    if rows[i]['Capa'] == 'I':
        interna.append(rows[i])
    
    elif rows[i]['Capa'] == 'M':
        middle.append(rows[i])
    
    elif rows[i]['Capa'] == 'E':
        externa.append(rows[i])
    
    elif rows[i]['Capa'] == 'M/I':
        middle.append(rows[i])
        interna.append(rows[i])
    
    elif rows[i]['Capa'] == 'M/E':
        middle.append(rows[i])
        externa.append(rows[i])

# Recopilación de datos necesarios para la optimización y establecimiento de la geometría

h_extprov = float(input("Viento en exterior (elegir número): 1 (interior tranquilo) / 2 (exterior sin viento) / 3 (brisa) / 4 (viento moderado) / 5 (viento fuerte): "))
h_intprov = float(input("Viento en interior (elegir número): 1 (interior tranquilo) / 2 (exterior sin viento) / 3 (brisa) / 4 (viento moderado) / 5 (viento fuerte): "))
t_ext = float(input("Temperatura del entorno (en Kelvin): "))
t_int = float(input("Temperatura de la capa interna (en Kelvin): "))
tct = float(input("Tiempo de comfort térmico"))
rango_temp = float(input("Rango de variación para temperatura de comfort (mínimo 1 grado): "))
if rango_temp < 1:
    print("El rango de variación debe ser de al menos 1 grado.")
    exit()
profundidad_1 = 0.002
profundidad_2 = 0.02
profundidad_3 = 0.002

# Cálculo de los coeficientes convectivos

if h_extprov == 1:
    h_ext = INTERIOR_TRANQUILO
elif h_extprov == 2:
    h_ext = EXTERIOR_SIN_VIENTO
elif h_extprov == 3:
    h_ext = BRISA
elif h_extprov == 4:
    h_ext = VIENTO_MODERADO
elif h_extprov == 5:
    h_ext = VIENTO_FUERTE

if h_intprov == 1:
    h_int = INTERIOR_TRANQUILO
elif h_intprov == 2:
    h_int = EXTERIOR_SIN_VIENTO
elif h_intprov == 3:
    h_int = BRISA
elif h_intprov == 4:
    h_int = VIENTO_MODERADO
elif h_intprov == 5:
    h_int = VIENTO_FUERTE

# Determinación de materiales que cumplen con el tct (tiempo de comfort térmico)

comb_cumplen = []
for i in interna:
    for e in externa:
        for m in middle: 
            
            # Definición de variables y establecimiento de la condición de estabilidad

            dn = 0.002
            k_1 = float(e['k'])
            c_1 = float(e['c'])
            rho_1 = float(e['rho'])
            alpha_1 = k_1 / (c_1 * rho_1)
            k_2 = float(m['k'])
            c_2 = float(m['c'])
            rho_2 = float(m['rho'])
            alpha_2 = k_2 / (c_2 * rho_2)
            k_3 = float(i['k'])
            c_3 = float(i['c'])
            rho_3 = float(i['rho'])
            alpha_3 = k_3 / (c_3 * rho_3)
            max_alpha = max(alpha_1, alpha_2, alpha_3)
            dt = 0.48 * dn**2 / max_alpha
            it = math.ceil(tct/dt)

            # Llamada al solver y determinación de cumplimiento con el tct

            if solver.resolver_termica(dn, dt, profundidad_1, profundidad_2, profundidad_3, k_1, k_2, k_3, c_1, c_2, c_3, rho_1, rho_2, rho_3, h_ext, h_int, t_ext, t_int, it, rango_temp):
                comb_cumplen.append((e, m, i))

# Llamar a optimizador.py

optimizador.optimizar(comb_cumplen, profundidad_1, profundidad_2, profundidad_3)