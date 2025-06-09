def procesar_archivo_placa(nombre_archivo):
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

def procesar_archivo_IP(nombre_archivo):
    resultados = []
    with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
        for num_linea, linea in enumerate(archivo, start=1):
            cadena = linea.strip()
            valida, posicion, error = es_IP_valido(cadena)

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

    if estado == 'q11':
        return True, None, None
    else:
        return False, len(cadena), "Cadena incompleta, terminó antes de llegar al estado final"

def es_IP_valido(cadena: str):
    estado = "q0"
    bloque = ""
    contador_puntos = 0

    for i, caracter in enumerate(cadena):

        if not (caracter.isdigit() or caracter == '.'):
            return False, i, f"Carácter inválido '{caracter}'"

        match estado:
            case "q0":
                if caracter.isdigit():
                    estado = "q1"
                    bloque += caracter
                elif caracter == '.':
                    return False, i, "No se puede comenzar con un punto"

            case "q1":
                if caracter.isdigit():
                    estado = "q3"
                    bloque += caracter
                elif caracter == '.':
                    if int(bloque) > 255:
                        return False, i, "Valor de bloque mayor a 255"
                    contador_puntos += 1
                    bloque = ""
                    estado = "q2"

            case "q2":
                if caracter.isdigit():
                    estado = "q6"
                    bloque += caracter
                elif caracter == '.':
                    return False, i, "Dos puntos seguidos no son válidos"

            case "q3":
                if caracter.isdigit():
                    estado = "q4"
                    bloque += caracter
                    if int(bloque) > 255:
                        return False, i, "Valor de bloque mayor a 255"
                elif caracter == '.':
                    if int(bloque) > 255:
                        return False, i, "Valor de bloque mayor a 255"
                    contador_puntos += 1
                    bloque = ""
                    estado = "q2"

            case "q4":
                if caracter.isdigit():
                    bloque += caracter
                    if int(bloque) > 255:
                        return False, i, "Valor de bloque mayor a 255"
                    estado = "q5"
                elif caracter == '.':
                    if int(bloque) > 255:
                        return False, i, "Valor de bloque mayor a 255"
                    contador_puntos += 1
                    bloque = ""
                    estado = "q2"

            case "q5":
                return False, i, "Estado inválido por formato"

            case "q6":
                if caracter.isdigit():
                    bloque += caracter
                    if int(bloque) > 255:
                        return False, i, "Valor de bloque mayor a 255"
                    estado = "q7"
                elif caracter == '.':
                    if int(bloque) > 255:
                        return False, i, "Valor de bloque mayor a 255"
                    contador_puntos += 1
                    bloque = ""
                    estado = "q9"

            case "q7":
                if caracter.isdigit():
                    bloque += caracter
                    if int(bloque) > 255:
                        return False, i, "Valor de bloque mayor a 255"
                    estado = "q8"
                elif caracter == '.':
                    if int(bloque) > 255:
                        return False, i, "Valor de bloque mayor a 255"
                    contador_puntos += 1
                    bloque = ""
                    estado = "q9"

            case "q8":
                if caracter == '.':
                    if int(bloque) > 255:
                        return False, i, "Valor de bloque mayor a 255"
                    contador_puntos += 1
                    bloque = ""
                    estado = "q9"
                else:
                    return False, i, "Después de 3 dígitos solo se espera punto"

            case "q9":
                if caracter.isdigit():
                    estado = "q10"
                    bloque += caracter
                elif caracter == '.':
                    return False, i, "Dos puntos seguidos no son válidos"

            case "q10":
                if caracter.isdigit():
                    estado = "q11"
                    bloque += caracter
                elif caracter == '.':
                    if int(bloque) > 255:
                        return False, i, "Valor de bloque mayor a 255"
                    estado = "q13"
                    bloque = ""
                    contador_puntos += 1

            case "q11":
                if caracter.isdigit():
                    bloque += caracter
                    if int(bloque) > 255:
                        return False, i, "Valor de bloque mayor a 255"
                    estado = "q12"
                elif caracter == '.':
                    if int(bloque) > 255:
                        return False, i, "Valor de bloque mayor a 255"
                    estado = "q13"
                    bloque = ""
                    contador_puntos += 1

            case "q12":
                if caracter == '.':
                    estado = "q13"
                    bloque = ""
                    contador_puntos += 1
                else:
                    return False, i, "Después de 3 dígitos solo se espera punto"

            case "q13":
                if caracter.isdigit():
                    estado = "q14"
                    bloque += caracter
                else:
                    return False, i, "Se esperaba un dígito en el último bloque"

            case "q14":
                if caracter.isdigit():
                    estado = "q15"
                    bloque += caracter
                elif caracter == '.':
                    return False, i, "IP con demasiados bloques"

            case "q15":
                if caracter.isdigit():
                    estado = "q16"
                    bloque += caracter
                    if int(bloque) > 255:
                        return False, i, "Valor de bloque mayor a 255"
                elif caracter == '.':
                    return False, i, "IP con demasiados bloques"

            case "q16":
                return False, i, "Caracteres extra después de IP válida"

    if estado in {"q14", "q15", "q16"} and contador_puntos == 3:
        if int(bloque) > 255:
            return False, i - 1, "Último bloque mayor a 255"
        return True, None, None
    else:
        return False, i - 1, "Formato incompleto o puntos faltantes"