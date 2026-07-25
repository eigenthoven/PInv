import csv
import math
import solver       

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

h_ext = float(input("Viento en exterior: (interior tranquilo / exterior sin viento / brisa / viento moderado / viento fuerte): "))
h_int = float(input("Viento en interior: (interior tranquilo / exterior sin viento / brisa / viento moderado / viento fuerte): "))
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

# Determinación de mejores combinaciones por precio y por peso

comb_metricas = []

for e, m, i in comb_cumplen:

    masa_e = float(e['rho']) * profundidad_1
    masa_m = float(m['rho']) * profundidad_2
    masa_i = float(i['rho']) * profundidad_3

    peso = masa_e + masa_m + masa_i

    precio = (
        masa_e * float(e['precio']) +
        masa_m * float(m['precio']) +
        masa_i * float(i['precio'])
    )

    comb_metricas.append((e, m, i, precio, peso))

# Orden por precio

comb_precio = sorted(comb_metricas, key=lambda x: x[3])
print("Primera mejor combinación por precio: ", comb_precio[0], "\n Segunda mejor combinación por precio: ", comb_precio[1], "\n Tercera mejor combinación por precio: " , comb_precio[2])

# Orden por peso

comb_peso = sorted(comb_metricas, key=lambda x: x[4])
print("Primera mejor combinación por peso: ", comb_peso[0], "\n Segunda mejor combinación por peso: ", comb_peso[1], "\n Tercera mejor combinación por peso: " , comb_peso[2])