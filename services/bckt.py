from flask import jsonify
# Definir los 8 movimientos posibles
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

def bckt_caminos(tamMatriz, origen, destino, agujerosNegros, estrellasGigantes, agujerosGusano,
                zonasRecarga, celdasCargaRequerida, cargaInicial, matrizInicial, soluciones, camino):
    if es_valido(origen[1], origen[0], tamMatriz, matrizInicial) and es_viable(origen[1], origen[0], matrizInicial, cargaInicial, agujerosNegros, celdasCargaRequerida, agujerosGusano):
        camino.append(origen[:])
        aux = matrizInicial[origen[1]][origen[0]]
        cargaOriginal = cargaInicial
        cargaInicial -= aux
        matrizInicial[origen[1]][origen[0]] = -1
        enEstrella = False
        print("Posición válida y viable:", origen)
        print("Cargando matriz:")
        print(imprimir_matriz(matrizInicial))
        print("Carga inicial:", cargaInicial)
        print("Camino actual:", camino)

        if origen == destino:
            
            soluciones.append(camino[:])
            for fila in matrizInicial:
                print(' '.join(str(celda) for celda in fila) + '\n', end='')

            print("Camino encontrado-------------------------------------------------:", camino)
            matrizInicial[origen[1]][origen[0]] = aux
            camino.pop()
            
            return

        for e in estrellasGigantes:
            if e[0] == origen[0] and e[1] == origen[1]:
                print("Está en estrella")
                enEstrella = True
                break

        for e in zonasRecarga:
            print("Verificando zona de recarga")
            print(f"Zona de recarga: {e[0]}, {e[1]}, {e[2]}")
            if e[0] == origen[0] and e[1] == origen[1]:
                print("Está en zona de recarga")
                cargaInicial *= e[2]
                break

        for e in agujerosGusano:
            if e["entrada"][0] == origen[0] and e["entrada"][1] == origen[0]:
                print("Está en agujero de gusano")
                costo = matrizInicial[origen[0]][origen[1]] + matrizInicial[e["salida"][0]][e["salida"][1]]
                origen[0], origen[1] = e["salida"][0], e["salida"][1]
                matrizInicial[origen[0]][origen[1]] = -1
                break
        
        for e in celdasCargaRequerida:
            if e["coordenada"][0] == origen[0] and e["coordenada"][1] == origen[1]:
                print("Está en celda de carga requerida")
                cargaInicial += aux
                break

        print(f'Carga después de procesar la posición {origen}: {cargaInicial}')
        if enEstrella:
            print("Está en estrella gigante")
            print("Entrando a backtracking con estrellas gigantes")
            agujeros_alrededor = buscar_ag(origen, MOVIMIENTOS, agujerosNegros)
            for agujero in agujeros_alrededor:
                if agujero in agujerosNegros:
                    idx = agujerosNegros.index(agujero)
                    agujerosNegros.pop(idx)
                    bckt_caminos(
                        tamMatriz, origen, destino, agujerosNegros, estrellasGigantes,
                        agujerosGusano, zonasRecarga, celdasCargaRequerida, cargaInicial, matrizInicial, soluciones, camino
                    )
                    agujerosNegros.insert(idx, agujero)
                    cargaInicial = cargaOriginal
                    
        for mov in MOVIMIENTOS:
            nueva_pos = [origen[0] + mov[0], origen[1] + mov[1]]
            print("Probando nueva posición:", nueva_pos)
            bckt_caminos(
                tamMatriz, nueva_pos, destino, agujerosNegros, estrellasGigantes,
                agujerosGusano, zonasRecarga, celdasCargaRequerida, cargaInicial, matrizInicial, soluciones, camino
            )
        
        cargaInicial = cargaOriginal
        print(f'Valor de auxiliar: {aux}')
        print("Retrocediendo desde:", origen)
        matrizInicial[origen[1]][origen[0]] = aux
        camino.pop()
        print("Volviendo atrás desde:", origen)
        print("Camino actual después de retroceder:", camino)
        print("Carga después de retroceder:", cargaInicial)
        print("Matriz después de retroceder:")
        print(imprimir_matriz(matrizInicial))
        
    return soluciones

def es_valido(fila, col, tamM, M):
    print("Validando posición:", (col, fila))
    if fila < 0 or fila >= tamM["filas"] or col < 0 or col >= tamM["columnas"] or M[fila][col] == -1:
        print(f"Posición inválida: ({col}, {fila}) fuera de los límites o bloqueada.")
        return False
    print(f"Posición ({col}, {fila}) es válida.")
    return True

def es_viable(fila, col, M, carga, agujerosNegros, cargasRequeridas, agujerosGusano):
    print(f"Verificando viabilidad de la posición ({col}, {fila}) con carga {carga}.")
    if M[fila][col] > carga: 
        print(f"Posición ({col}, {fila}) no viable: carga insuficiente. Necesita {M[fila][col]}, tiene {carga}.")
        return False
    print(f"Posición ({col}, {fila}) tiene carga suficiente: {M[col][fila]} <= {carga}.")
    
    for e in agujerosNegros:
        if e[0] == col and e[1] == fila: 
            print(f"Posición ({col}, {fila}) no viable: agujero negro presente.")
            return False
    print(f'En la posción ({col}, {fila}) no hay agujeros negros.')
    
    
    for e in cargasRequeridas:
        if e["coordenada"][0] == col and e["coordenada"][1] == fila:
            if e["cargaMinima"] > carga:
                print(f"Posición ({col}, {fila}) no viable: carga mínima requerida no cumplida. Necesita {e['cargaMinima']}, tiene {carga}.")
                return False
            break
    print(f'La casilla no requiere carga')
    
    for e in agujerosGusano:
        if e["entrada"][0] == col and e["entrada"][1] == fila:
            costo = M[col][fila] + M[e["salida"][0]][e["salida"][1]]
            if costo > carga:
                print(f"Posición ({col}, {fila}) no viable: carga insuficiente para agujero de gusano.")
                return False
            break
    print(f"Posición ({col}, {fila}) es viable.")
    return True

def buscar_ag(origen, movimientos, agujerosNegros):
    agujeros = []
    for mov in movimientos:
        posPosible = [origen[0] + mov[0], origen[1] + mov[1]]
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
    # # print(matriz)
    # print("solucioneses encontradas:")
    # for sol in solucioneses:
    #     print(sol)
        