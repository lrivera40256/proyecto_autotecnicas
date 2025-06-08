from flask import jsonify
# Definir los 8 movimientos posibles
# (columna, fila)
MOVIMIENTOS = [
    (0, -1),  # Arriba
    (1,-1),  # Arriba derecha
    (1, 0),  # Derecha
    (1, 1),  # Abajo derecha
    (0, 1),  # Abajo
    (-1, 1),  # Abajo izquierda
    (-1, 0),  # Izquierda
    (-1, -1)  # Arriba izquierda
]

def imprimir_matriz(matriz):
    for fila in matriz:
        print(' '.join(str(celda) for celda in fila))
    print()

def bckt_caminos(tamMatriz, posAct, destino, agujerosNegros, estrellasGigantes, agujerosGusano,
                zonasRecarga, celdasCargaRequerida, cargaActual, matrizInicial, soluciones, camino):
    if es_valido(posAct[1], posAct[0], tamMatriz, matrizInicial) and es_viable(posAct[1], posAct[0], matrizInicial, cargaActual, agujerosNegros, celdasCargaRequerida, agujerosGusano):
        print(destino == posAct, "------------------------------------------------------------------------------------------------------")
        camino.append(posAct[:])
        aux = matrizInicial[posAct[1]][posAct[0]]   # Guardar el valor original de la celda
        cargaOriginal = cargaActual                 # Guardar la carga inicial
        cargaActual -= aux
        matrizInicial[posAct[1]][posAct[0]] = -1
        enEstrella = False
        print("Posición válida y viable:", posAct)
        print("Cargando matriz:")
        # print(imprimir_matriz(matrizInicial))
        print("Carga inicial:", cargaActual)
        print("Camino actual:", camino)

        if posAct == destino:
            
            soluciones.append(camino[:])
            # for fila in matrizInicial:
            #     print(' '.join(str(celda) for celda in fila) + '\n', end='')

            print("Camino encontrado-------------------------------------------------:", camino)
            # matrizInicial[posAct[1]][posAct[0]] = aux
            # camino.pop()
            return camino[:]

        idx_estrella = None
        for i, e in enumerate(estrellasGigantes):
            if e[0] == posAct[0] and e[1] == posAct[1]:
                print("Está en estrella")
                enEstrella = True
                idx_estrella = i 
                break

        for e in zonasRecarga:
            print("Verificando zona de recarga")
            if e[0] == posAct[0] and e[1] == posAct[1]:
                print(f"Zona de recarga: {e[0]}, {e[1]}, {e[2]}")
                print("Está en zona de recarga")
                print(f'Carga inicial: {cargaActual}')
                cargaActual += aux
                cargaActual *= e[2]
                print(f'Carga después de recarga: {cargaActual}')
                break

        for e in agujerosGusano:
            if e[0][0] == posAct[0] and e[0][1] == posAct[1]:
                print(f"Está en agujero de gusano: {e[0]}")
                bckt_caminos(
                tamMatriz, e[1], destino, agujerosNegros, estrellasGigantes,
                agujerosGusano, zonasRecarga, celdasCargaRequerida, cargaActual, matrizInicial, soluciones, camino
                )
                break
            

        print(f'Carga después de procesar la posición {posAct}: {cargaActual}')
        if enEstrella:
            print("Está en estrella gigante")
            print("Entrando a backtracking con estrellas gigantes")
            agujeros_alrededor = buscar_ag(posAct, agujerosNegros)
            print(agujeros_alrededor)
            for agujero in agujeros_alrededor:
                idx_agujero = agujerosNegros.index(agujero)
                agujerosNegros.pop(idx_agujero)
                estrellasGigantes.pop(idx_estrella)
                bckt_caminos(
                    tamMatriz, agujero, destino, agujerosNegros, estrellasGigantes,
                    agujerosGusano, zonasRecarga, celdasCargaRequerida, cargaActual, matrizInicial, soluciones, camino
                )
                agujerosNegros.insert(idx_agujero, agujero)
                estrellasGigantes.insert(idx_estrella, agujero)

        for mov in MOVIMIENTOS:
            nueva_pos = [posAct[0] + mov[0], posAct[1] + mov[1]]
            print("Probando nueva posición:", nueva_pos)
            bckt_caminos(
                tamMatriz, nueva_pos, destino, agujerosNegros, estrellasGigantes,
                agujerosGusano, zonasRecarga, celdasCargaRequerida, cargaActual, matrizInicial, soluciones, camino
            )
        
        cargaActual = cargaOriginal
        print(f'Valor de auxiliar: {aux}')
        print("Retrocediendo desde:", posAct)
        matrizInicial[posAct[1]][posAct[0]] = aux
        camino.pop()
        print("Volviendo atrás desde:", posAct)
        print("Camino actual después de retroceder:", camino)
        print("Carga después de retroceder:", cargaActual)
        print("Matriz después de retroceder:")
        # print(imprimir_matriz(matrizInicial))
    return soluciones

def es_valido(fila, col, tamM, M):
    print("Validando posición:", (col, fila))
    if fila < 0 or fila >= tamM[1] or col < 0 or col >= tamM[0] or M[fila][col] == -1:
        print(f"Posición inválida: ({col}, {fila}) fuera de los límites o bloqueada.")
        return False
    print(f"Posición ({col}, {fila}) es válida.")
    return True

def es_viable(fila, col, M, carga, agujerosNegros, cargasRequeridas, agujerosGusano):
    print(f"Verificando viabilidad de la posición ({col}, {fila}) con carga {carga}.")
    if M[fila][col] > carga:
        print(f"Posición ({col}, {fila}) no viable: carga insuficiente. Necesita {M[fila][col]}, tiene {carga}.")
        return False
    print(f"Posición ({col}, {fila}) tiene carga suficiente: {M[fila][col]} <= {carga}.")
    
    for e in agujerosNegros:
        if e[0] == col and e[1] == fila: 
            print(f"Posición ({col}, {fila}) no viable: agujero negro presente.")
            return False
    print(f'En la posción ({col}, {fila}) no hay agujeros negros.')
    
    for e in cargasRequeridas:
        if e[0][0] == col and e[0][1] == fila:
            if e[1] > carga:
                print(f"Posición ({col}, {fila}) no viable: carga mínima requerida no cumplida. Necesita {e['cargaGastada']}, tiene {carga}.")
                return False
            break
    print(f'La casilla no requiere carga')
    
    for e in agujerosGusano:
        if e[0][0] == col and e[0][1] == fila:
            costo = M[fila][col] + M[e[1][1]][e[1][0]]
            if costo > carga:
                print(f"Posición ({col}, {fila}) no viable: carga insuficiente para agujero de gusano.")
                return False
            break
    print(f"Posición ({col}, {fila}) es viable.")
    return True

def buscar_ag(posAct, agujerosNegros):
    agujeros = []
    for mov in MOVIMIENTOS:
        posPosible = [posAct[0] + mov[0], posAct[1] + mov[1]]
        if posPosible in agujerosNegros:
            agujeros.append(posPosible)
    return agujeros

def lector_json(ruta):
    import json
    with open(ruta, 'r') as file:
        data = json.load(file)
    return data

if __name__ == "__main__":
    matriz = lector_json('data/test5x5.json')
    solucioneses = bckt_caminos(**matriz)
