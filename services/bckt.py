import copy
from flask import jsonify

MOVIMIENTOS = [
    (0, -1),  # Arriba
    (1, -1),  # Arriba derecha
    (1, 0),   # Derecha
    (1, 1),   # Abajo derecha
    (0, 1),   # Abajo
    (-1, 1),  # Abajo izquierda
    (-1, 0),  # Izquierda
    (-1, -1)  # Arriba izquierda
]

def imprimir_matriz(matriz):
    for fila in matriz:
        print(fila)
    print()

def bckt_caminos(tamMatriz, posAct, destino, agujerosNegros, estrellasGigantes, agujerosGusano,
                 zonasRecarga, celdasCargaRequerida, cargaActual, matrizInicial, soluciones, camino):
    if len(soluciones) >= 5:
        return True

    print(f"Posición actual: {posAct}, Carga: {cargaActual}")

    if es_valido(posAct[1], posAct[0], tamMatriz, matrizInicial) and es_viable(posAct[1], posAct[0], matrizInicial, cargaActual, agujerosNegros, celdasCargaRequerida, agujerosGusano):
        camino.append(posAct[:])
        aux = matrizInicial[posAct[1]][posAct[0]]
        cargaOriginal = cargaActual
        cargaActual -= aux
        matrizInicial[posAct[1]][posAct[0]] = -1

        enEstrella = False
        idx_estrella = None

        if posAct == destino:
            print("Solución encontrada:")
            print(camino)
            soluciones.append(copy.deepcopy(camino))
            matrizInicial[posAct[1]][posAct[0]] = aux
            camino.pop()
            return len(soluciones) >= 5

        for i, e in enumerate(estrellasGigantes):
            if e[0] == posAct[0] and e[1] == posAct[1]:
                enEstrella = True
                idx_estrella = i
                break

        for e in zonasRecarga:
            if e[0] == posAct[0] and e[1] == posAct[1]:
                print("Zona de recarga encontrada")
                cargaActual += aux
                cargaActual *= e[2]
                break

        for e in agujerosGusano:
            if e[0][0] == posAct[0] and e[0][1] == posAct[1]:
                print("Agujero de gusano activado")
                if bckt_caminos(tamMatriz, e[1], destino, agujerosNegros, estrellasGigantes,
                                agujerosGusano, zonasRecarga, celdasCargaRequerida,
                                cargaActual, matrizInicial, soluciones, camino):
                    if len(soluciones) >= 5:
                        return True
                break

        if enEstrella:
            print("Estrella gigante activada")
            agujeros_alrededor = buscar_ag(posAct, agujerosNegros)
            for agujero in agujeros_alrededor:
                idx_agujero = agujerosNegros.index(agujero)
                agujerosNegros.pop(idx_agujero)
                estrellasGigantes.pop(idx_estrella)
                if bckt_caminos(tamMatriz, agujero, destino, agujerosNegros, estrellasGigantes,
                                agujerosGusano, zonasRecarga, celdasCargaRequerida,
                                cargaActual, matrizInicial, soluciones, camino):
                    if len(soluciones) >= 5:
                        return True
                agujerosNegros.insert(idx_agujero, agujero)
                estrellasGigantes.insert(idx_estrella, posAct)

        for mov in MOVIMIENTOS:
            nueva_pos = [posAct[0] + mov[0], posAct[1] + mov[1]]
            if bckt_caminos(tamMatriz, nueva_pos, destino, agujerosNegros, estrellasGigantes,
                            agujerosGusano, zonasRecarga, celdasCargaRequerida,
                            cargaActual, matrizInicial, soluciones, camino):
                if len(soluciones) >= 5:
                    return True

        cargaActual = cargaOriginal
        matrizInicial[posAct[1]][posAct[0]] = aux
        camino.pop()
    return False

def es_valido(fila, col, tamM, M):
    return not (fila < 0 or fila >= tamM[1] or col < 0 or col >= tamM[0] or M[fila][col] == -1)

def es_viable(fila, col, M, carga, agujerosNegros, cargasRequeridas, agujerosGusano):
    if M[fila][col] > carga:
        return False
    for e in agujerosNegros:
        if e[0] == col and e[1] == fila:
            return False
    for e in cargasRequeridas:
        if e[0][0] == col and e[0][1] == fila and e[1] > carga:
            return False
    for e in agujerosGusano:
        if e[0][0] == col and e[0][1] == fila:
            costo = M[fila][col] + M[e[1][1]][e[1][0]]
            if costo > carga:
                return False
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

# Ejemplo de ejecución
# if __name__ == "__main__":
#     matriz = lector_json('data/test5x5.json')
#     soluciones = []
#     bckt_caminos(matriz['tamMatriz'],
#                  matriz['origen'],
#                  matriz['destino'],
#                  matriz['agujerosNegros'],
#                  matriz['estrellasGigantes'],
#                  matriz['agujerosGusano'],
#                  matriz['zonasRecarga'],
#                  matriz['celdasCargaRequerida'],
#                  matriz['cargaInicial'],
#                  matriz['matrizInicial'],
#                  soluciones,
#                  [])
#     print(f"{len(soluciones)} soluciones encontradas.")
#     for s in soluciones:
#         print(s)
