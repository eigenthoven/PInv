def optimizar(comb_cumplen, profundidad_1, profundidad_2, profundidad_3):

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