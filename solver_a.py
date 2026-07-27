import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def resolver_termica(dn, dt, profundidad_1, profundidad_2, profundidad_3, k_1, k_2, k_3, c_1, c_2, c_3, rho_1, rho_2, rho_3, h_ext, h_int, t_ext, t_int, it):

    # Cálculo de parámetros secundarios y condiciones de estabilidad

    alpha_1 = k_1 / (c_1 * rho_1)
    alpha_2 = k_2 / (c_2 * rho_2)
    alpha_3 = k_3 / (c_3 * rho_3)
    profundidad = profundidad_1 + profundidad_2 + profundidad_3
    N = int(profundidad / dn) + 1
    r_1 = (dt * alpha_1) / dn**2
    r_2 = (dt * alpha_2) / dn**2
    r_3 = (dt * alpha_3) / dn**2

    # Comprobación de estabilidad del método FTCS

    if max(r_1, r_2, r_3) >= 0.5:
        print("El método FTCS no es estable.")
        return

    # Creación de la malla de cálculo

    T = np.full(N, t_int)
    T[0] = t_ext
    T[-1] = t_int

    # Creación del historial de temperaturas

    history = [T.copy()]

    # Resolución de la evolución térmica

    for _ in range(it):
        T_new = T.copy()

        # Convección en fronteras según Ley de Enfriamiento de Newton y Condición de Robin

        T_new[0] = ((k_1 / dn) * T[1] + h_ext * t_ext) / (k_1 / dn + h_ext)
        T_new[-1] = ((k_3 / dn) * T[-2] + h_int * t_int) / (k_3 / dn + h_int)

        # Conducción en las capas interiores según la ecuación de calor y FTCS

        for j in range(1, N - 1):

            if j < profundidad_1 / dn + 1:
                T_new[j] = r_1 * (T[j + 1] - 2 * T[j] + T[j - 1]) + T[j]

            elif j == profundidad_1 / dn + 1:
                T_new[j] = (k_1 * T[j - 1] + k_2 * T[j + 1]) / (k_1 + k_2)

            elif j < profundidad_1 / dn + profundidad_2 / dn + 1:
                T_new[j] = r_2 * (T[j + 1] - 2 * T[j] + T[j - 1]) + T[j]

            elif j == profundidad_1 / dn + profundidad_2 / dn + 1:
                T_new[j] = (k_2 * T[j - 1] + k_3 * T[j + 1]) / (k_2 + k_3)

            else:
                T_new[j] = r_3 * (T[j + 1] - 2 * T[j] + T[j - 1]) + T[j]

        # Actualización de malla

        T = T_new

        # Actualización del historial de temperaturas

        history.append(T.copy())


    # Animación de la evolución térmica

    history = np.array(history)

    y = np.linspace(0, profundidad, N)

    fig, ax = plt.subplots(figsize=(10, 6))

    line, = ax.plot(
        y,
        history[0]
    )

    # Representación de las interfaces entre capas

    ax.axvline(
        profundidad_1,
        linestyle="--",
        linewidth=2
    )

    ax.axvline(
        profundidad_1 + profundidad_2,
        linestyle="--",
        linewidth=2
    )

    ax.set_xlabel("Profundidad (m)")
    ax.set_ylabel("Temperatura (K)")

    ax.set_title(
        "Evolución térmica en pared multicapa"
    )

    ax.set_xlim(
        0,
        profundidad
    )

    ax.set_ylim(
        np.min(history),
        np.max(history)
    )

    def update(frame):

        line.set_ydata(history[frame])

        ax.set_title(
            f"Evolución térmica en pared multicapa | "
            f"t = {frame * dt:.2f} s"
        )

        return [line]

    ani = FuncAnimation(
        fig,
        update,
        frames=len(history),
        interval=40,
        blit=False
    )

    plt.show()