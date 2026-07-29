def optimizar(comb_cumplen, profundidad_1, profundidad_2, profundidad_3):

    # Determinación de ponderación de criterios (peso y precio)

    peso_pond = float(input("Introducir el peso de la variable 'peso' (entre 0 y 1); el peso de la variable 'precio' se calcula a partir de este valor: "))
    precio_pond = 1 - peso_pond

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

    # Normalización y cálculo de puntuación ponderada

    precio_max = max(x[3] for x in comb_metricas)
    peso_max = max(x[4] for x in comb_metricas)
    comb_optimas = []

    for e, m, i, precio, peso in comb_metricas:
        precio_norm = precio / precio_max
        peso_norm = peso / peso_max
        puntuacion = precio_pond * precio_norm + peso_pond * peso_norm
        comb_optimas.append((e, m, i, precio, peso, puntuacion))

    # Orden por puntuación ponderada

    comb_optimas = sorted(comb_optimas, key=lambda x: x[5])

    print("Primera mejor combinación global: ", comb_optimas[0], "\n Segunda mejor combinación global: ", comb_optimas[1], "\n Tercera mejor combinación global: ", comb_optimas[2])