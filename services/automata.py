def procesar_archivo(nombre_archivo):
    resultados = []
    with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
        for num_linea, linea in enumerate(archivo, start=1):
            cadena = linea.strip()
            valida, posicion, error = es_placa_valida(cadena)

            if valida:
                resultados.append(f"Línea {num_linea}: ✔️ Válida → {cadena}")
            else:
                if posicion is not None and posicion < len(cadena):
                    caracter_error = cadena[posicion]
                    resultados.append(f"Línea {num_linea}: ❌ Inválida → '{cadena}'")
                    resultados.append(f"  Error en posición {posicion + 1}: '{caracter_error}' → {error}")
                else:
                    resultados.append(f"Línea {num_linea}: ❌ Inválida → '{cadena}'")
                    resultados.append(f"  Error: {error}")
    return resultados

def es_placa_valida(cadena: str):
    estado = 'q0'
    for i, caracter in enumerate(cadena):
        match estado:
            case 'q0':
                if caracter.isalpha() and caracter.isupper():
                    estado = 'q2'
                else:
                    return False, i, "Se esperaba una letra mayúscula al inicio"

            case 'q2':
                if caracter.isalpha() and caracter.isupper():
                    estado = 'q3'
                else:
                    return False, i, "Se esperaba la segunda letra mayúscula"

            case 'q3':
                if caracter.isalpha() and caracter.isupper():
                    estado = 'q4'
                else:
                    return False, i, "Se esperaba la tercera letra mayúscula"

            case 'q4':
                if caracter == '-':
                    estado = 'q5'
                else:
                    return False, i, "Se esperaba un guion (-) después de las letras"

            case 'q5':
                if caracter.isdigit():
                    estado = 'q6'
                else:
                    return False, i, "Se esperaba un dígito (1 de 4)"

            case 'q6':
                if caracter.isdigit():
                    estado = 'q7'
                else:
                    return False, i, "Se esperaba un dígito (2 de 4)"

            case 'q7':
                if caracter.isdigit():
                    estado = 'q8'
                else:
                    return False, i, "Se esperaba un dígito (3 de 4)"

            case 'q8':
                if caracter.isdigit():
                    estado = 'q9'
                else:
                    return False, i, "Se esperaba un dígito (4 de 4)"

            case 'q9':
                if caracter == '-':
                    estado = 'q10'
                else:
                    return False, i, "Se esperaba un guion (-) antes del tipo de vehículo"

            case 'q10':
                if caracter.isalpha() and caracter.isupper():
                    estado = 'q11'
                else:
                    return False, i, "Se esperaba una letra mayúscula como tipo de vehículo"

            case 'q11':
                return False, i, "Demasiados caracteres después del estado final"

    # Validación final
    if estado == 'q11':
        return True, None, None
    else:
        return False, len(cadena), "Cadena incompleta, terminó antes de llegar al estado final"

procesar_archivo('data/placas.txt')