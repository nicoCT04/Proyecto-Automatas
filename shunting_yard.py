"""
Implementación del algoritmo Shunting Yard para convertir expresiones regulares a notación postfix
"""


alfabeto = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@._!?-, ')

def procesar_escapes(expresion):
    """
    Procesa secuencias de escape y clases de caracteres en la expresión regular
    Convierte \\. en ● (punto literal usando símbolo especial)
    Convierte [ae03] en (a|e|0|3)
    """
    resultado = []
    i = 0
    while i < len(expresion):
        if i < len(expresion) - 1 and expresion[i] == '\\':
            # Carácter escapado
            if expresion[i + 1] == '.':
                resultado.append('●')  # Punto literal usando símbolo especial
                i += 2
            elif expresion[i + 1] == '?':
                resultado.append('◆')  # Signo de interrogación literal usando símbolo especial
                i += 2
            elif expresion[i + 1] == '(':
                resultado.append('◎')  # Paréntesis izquierdo literal
                i += 2
            elif expresion[i + 1] == ')':
                resultado.append('◉')  # Paréntesis derecho literal
                i += 2
            elif expresion[i + 1] == '\\':
                resultado.append('◈')  # Barra invertida literal
                i += 2
            elif expresion[i + 1] == '{':
                resultado.append('◊')  # Llave izquierda literal
                i += 2
            elif expresion[i + 1] == '}':
                resultado.append('◘')  # Llave derecha literal
                i += 2
            else:
                # Otros escapes - convertir a literal quitando la barra
                resultado.append(expresion[i + 1])
                i += 2
        elif expresion[i] == '[':
            # Clase de caracteres - encontrar el final
            j = i + 1
            while j < len(expresion) and expresion[j] != ']':
                j += 1
            if j < len(expresion):
                # Extraer caracteres dentro de la clase
                caracteres_clase = expresion[i+1:j]
                # Convertir a unión: [ae03] -> (a|e|0|3)
                if len(caracteres_clase) > 1:
                    union = '(' + '|'.join(caracteres_clase) + ')'
                else:
                    union = caracteres_clase  # Solo un carácter
                resultado.append(union)
                i = j + 1
            else:
                # [ sin cierre - tratarlo como símbolo literal
                resultado.append(expresion[i])
                i += 1
        else:
            resultado.append(expresion[i])
            i += 1
    return ''.join(resultado)

def convertir_a_postfix(expresion):
    """
    Convierte una expresión regular a notación postfix usando el algoritmo Shunting Yard
    """
    # Precedencia de operadores (mayor número = mayor precedencia)
    # El punto . (comodín) se trata como un operando especial, no como operador
    precedencia = {'|': 1, '·': 2, '*': 3, '+': 3, '?': 3}
    
    # Preprocesar la expresión para manejar escapes y agregar operadores de concatenación explícitos
    expresion_procesada = procesar_escapes(expresion)
    expresion_procesada = agregar_concatenacion(expresion_procesada)
    
    pila_operadores = []
    salida = []
    
    for caracter in expresion_procesada:
        if caracter == '(':
            # Si es paréntesis izquierdo, agregarlo a la pila
            pila_operadores.append(caracter)
        elif caracter == ')':
            # Si es paréntesis derecho, vaciar hasta encontrar el izquierdo
            while pila_operadores and pila_operadores[-1] != '(':
                salida.append(pila_operadores.pop())
            if pila_operadores:
                pila_operadores.pop()  # Quitar el '('
        elif caracter in precedencia:
            # Si es un operador (verificar ANTES que símbolo)
            while (pila_operadores and 
                   pila_operadores[-1] != '(' and
                   pila_operadores[-1] in precedencia and
                   precedencia[pila_operadores[-1]] >= precedencia[caracter]):
                salida.append(pila_operadores.pop())
            pila_operadores.append(caracter)
        elif es_simbolo(caracter):
            # Si es un símbolo del alfabeto, agregarlo a la salida
            salida.append(caracter)
    
    # Vaciar la pila de operadores restantes
    while pila_operadores:
        salida.append(pila_operadores.pop())
    
    return ''.join(salida)

def agregar_concatenacion(expresion):
    """
    Agrega operadores de concatenación explícitos (·) donde sean necesarios
    """
    resultado = []
    
    for i in range(len(expresion)):
        actual = expresion[i]
        resultado.append(actual)
        
        if i < len(expresion) - 1:
            siguiente = expresion[i + 1]
            
            # NO agregar concatenación si:
            # - El siguiente carácter es un operador binario (|)
            # - El actual es un operador binario (|)
            if siguiente == '|' or actual == '|':
                continue
            
            # Agregar concatenación solo cuando es necesario
            
            necesita_concatenacion = False
            
            if es_simbolo(actual) and es_simbolo(siguiente):
                necesita_concatenacion = True
            elif es_simbolo(actual) and siguiente == '(':
                necesita_concatenacion = True
            elif actual == ')' and es_simbolo(siguiente):
                necesita_concatenacion = True
            elif actual == ')' and siguiente == '(':
                necesita_concatenacion = True
            elif actual in '*+?' and es_simbolo(siguiente):
                necesita_concatenacion = True
            elif actual in '*+?' and siguiente == '(':
                necesita_concatenacion = True
            
            if necesita_concatenacion:
                resultado.append('·')
    
    return ''.join(resultado)

def es_simbolo(caracter):
    """
    Determina si un carácter es un símbolo del alfabeto
    (letras, dígitos, épsilon, @, símbolos especiales, etc.)
    """
    # Operadores y metacaracteres reservados del regex
    operadores_reservados = {'|', '·', '*', '+', '(', ')', '[', ']', '\\', '?'}
    
    # Un símbolo es cualquier carácter que NO sea un operador reservado
    return caracter not in operadores_reservados

def mostrar_conversion(expresion):
    """
    Muestra el proceso de conversión de infix a postfix
    """
    print(f"Expresión original: {expresion}")
    
    # Procesar en el mismo orden que convertir_a_postfix
    expresion_procesada = procesar_escapes(expresion)
    expresion_con_concat = agregar_concatenacion(expresion_procesada)
    print(f"Con concatenación explícita: {expresion_con_concat}")
    
    resultado = convertir_a_postfix(expresion)
    print(f"Notación postfix: {resultado}")
    return resultado
