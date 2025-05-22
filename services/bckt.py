def bckt_caminos(tamMatriz, origen, destino, agujerosNegros, estrellasGigantes, agujerosGusano, zonasRecarga, celdasCargaRequerida, cargaInicial, matrizInicial):
    print(f'Tamaño matriz: {tamMatriz} ({type(tamMatriz).__name__})')
    print(f'Origen: {origen} ({type(origen).__name__})')
    print(f'Destino: {destino} ({type(destino).__name__})')
    print(f'Agujeros Negros: {agujerosNegros} ({type(agujerosNegros).__name__})')
    print(f'Estrellas Gigantes: {estrellasGigantes} ({type(estrellasGigantes).__name__})')
    print(f'Agujeros Gusano: {agujerosGusano} ({type(agujerosGusano).__name__})')
    print(f'Zonas Recarga: {zonasRecarga} ({type(zonasRecarga).__name__})')
    print(f'Celdas Carga Requerida: {celdasCargaRequerida} ({type(celdasCargaRequerida).__name__})')
    print(f'Carga Inicial: {cargaInicial} ({type(cargaInicial).__name__})')
    print(f'Matriz Inicial: {matrizInicial} ({type(matrizInicial).__name__})')

    camino = [(0, 0), (0, 1), (1, 1)]
    return camino
