import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Parámetros de entrada

dn = float(input("Incremento de espacio (tanto dx como dy): "))
dt = float(input("Incremento de tiempo: "))
longitud = float(input("Longitud de la sección de pared: "))
profundidad_1 = float(input("Profundidad de capa externa: "))
profundidad_2 = float(input("Profundidad de capa intermedia: "))
profundidad_3 = float(input("Profundidad de capa interna: "))
k_1 = float(input("Conductividad térmica (capa externa; coherente con difusividad térmica de la capa externa): "))
k_2 = float(input("Conductividad térmica (capa intermedia; coherente con difusividad térmica de la capa intermedia): "))
k_3 = float(input("Conductividad térmica (capa interna; coherente con difusividad térmica de la capa interna): "))
c_1 = float(input("Capacidad calorífica (capa externa): "))
c_2 = float(input("Capacidad calorífica (capa intermedia): "))
c_3 = float(input("Capacidad calorífica (capa interna): "))
rho_1 = float(input("Densidad (capa externa): "))
rho_2 = float(input("Densidad (capa intermedia): "))
rho_3 = float(input("Densidad (capa interna): "))
h_ext = float(input("Coeficiente de convección (capa externa): "))
h_int = float(input("Coeficiente de convección (capa interna): "))
t_ext = float(input("Temperatura del entorno (en Kelvin): "))
t_int = float(input("Temperatura inicial de la pared y el interior (en Kelvin): "))
it = int(input("Número de interaciones: "))

# Cálculo de parámetros secundarios y condiciones de estabilidad

alpha_1 = k_1 / (c_1 * rho_1)
alpha_2 = k_2 / (c_2 * rho_2)
alpha_3 = k_3 / (c_3 * rho_3)
profundidad = profundidad_1 + profundidad_2 + profundidad_3
N_y = int(profundidad/dn) + 1
N_x = int(longitud/dn) + 1
r_1 = (dt * alpha_1)/dn**2
r_2 = (dt * alpha_2)/dn**2
r_3 = (dt * alpha_3)/dn**2

if max(r_1, r_2, r_3) >= 0.25:
    print("El método no es estable.")
    exit()

# Creación de la malla 2D de cálculo

T = np.full((int(profundidad/dn) + 1, int(longitud/dn) + 1), t_int)
T[0, :] = t_ext
T[-1, :] = t_int

# Creación del historial de animación

history = [T.copy()]

# Resolución de la evolución térmica

for _ in range(it):
    T_new = T.copy()

    # Convección en fronteras según Ley de Enfriamiento de Newton y Condición de Robin

    for i in range(1, N_x - 1):
        T_new[0, i] = ((k_1/dn) * T[1, i] + h_ext * t_ext) / (k_1/dn + h_ext)
        T_new[-1, i] = ((k_3/dn) * T[-2, i] + h_int * t_int) / (k_3/dn + h_int)
    
    # Conducción en las capas interiores según la ecuación de calor y FTCS

    for j in range(1, N_y - 1):
        for i in range(1, N_x - 1):
            if j < profundidad_1/dn + 1:
                T_new[j, i] = r_1*(T[j, i + 1] + T[j + 1, i] - 4*T[j,i] + T[j, i - 1] + T[j - 1, i]) + T[j,i]
            elif j == profundidad_1/dn + 1:
                T_new[j, i] = (k_1 * T[j - 1, i] + k_2 * T[j + 1, i]) / (k_1 + k_2)
            elif j < profundidad_1/dn + profundidad_2/dn + 1:
                T_new[j, i] = r_2*(T[j, i + 1] + T[j + 1, i] - 4*T[j,i] + T[j, i - 1] + T[j - 1, i]) + T[j,i]
            elif j == profundidad_1/dn + profundidad_2/dn + 1:
                T_new[j, i] = (k_2 * T[j - 1, i] + k_3 * T[j + 1, i]) / (k_2 + k_3)
            else:
                T_new[j, i] = r_3*(T[j, i + 1] + T[j + 1, i] - 4*T[j,i] + T[j, i - 1] + T[j - 1, i]) + T[j,i]
    
    # Actualización de malla y animación

    T = T_new
    history.append(T.copy())

# Animación (ChatGPT)

fig, ax = plt.subplots(figsize=(10, 6))

im = ax.imshow(
    history[0],
    origin="upper",
    extent=[0, longitud, profundidad, 0],
    cmap="coolwarm",
    aspect="auto",
    vmin=np.min(history),
    vmax=np.max(history)
)

cbar = plt.colorbar(im)
cbar.set_label("Temperatura (K)")

ax.axhline(profundidad_1, color="black", linestyle="--", linewidth=2)
ax.axhline(profundidad_1 + profundidad_2, color="black", linestyle="--", linewidth=2)

ax.set_xlabel("Longitud (m)")
ax.set_ylabel("Profundidad (m)")
ax.set_title("Evolución térmica en medio multicapa")

def update(frame):
    im.set_array(history[frame])
    ax.set_title(f"Evolución térmica | t = {frame * dt:.2f} s")
    return [im]

ani = FuncAnimation(
    fig,
    update,
    frames=len(history),
    interval=40,
    blit=False
)

plt.show()