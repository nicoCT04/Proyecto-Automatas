"""
Implementación del algoritmo Shunting Yard para convertir expresiones regulares a notación postfix
"""

def convertir_a_postfix(expresion):
    """
    Convierte una expresión regular a notación postfix usando el algoritmo Shunting Yard
    """
    # Precedencia de operadores (mayor número = mayor precedencia)
    precedencia = {'|': 1, '.': 2, '*': 3, '+': 3}
    
    # Preprocesar la expresión para agregar operadores de concatenación explícitos
    expresion_procesada = agregar_concatenacion(expresion)
    
    pila_operadores = []
    salida = []
    
    for caracter in expresion_procesada:
        if es_simbolo(caracter):
            # Si es un símbolo del alfabeto, agregarlo a la salida
            salida.append(caracter)
        elif caracter == '(':
            # Si es paréntesis izquierdo, agregarlo a la pila
            pila_operadores.append(caracter)
        elif caracter == ')':
            # Si es paréntesis derecho, vaciar hasta encontrar el izquierdo
            while pila_operadores and pila_operadores[-1] != '(':
                salida.append(pila_operadores.pop())
            if pila_operadores:
                pila_operadores.pop()  # Quitar el '('
        elif caracter in precedencia:
            # Si es un operador
            while (pila_operadores and 
                   pila_operadores[-1] != '(' and
                   pila_operadores[-1] in precedencia and
                   precedencia[pila_operadores[-1]] >= precedencia[caracter]):
                salida.append(pila_operadores.pop())
            pila_operadores.append(caracter)
    
    # Vaciar la pila de operadores restantes
    while pila_operadores:
        salida.append(pila_operadores.pop())
    
    return ''.join(salida)

def agregar_concatenacion(expresion):
    """
    Agrega operadores de concatenación explícitos (.) donde sean necesarios
    """
    resultado = []
    
    for i in range(len(expresion)):
        resultado.append(expresion[i])
        
        if i < len(expresion) - 1:
            actual = expresion[i]
            siguiente = expresion[i + 1]
            
            # Agregar concatenación entre:
            # - símbolo y símbolo
            # - símbolo y paréntesis izquierdo
            # - paréntesis derecho y símbolo
            # - paréntesis derecho y paréntesis izquierdo
            # - operador unario (*,+) y símbolo
            # - operador unario (*,+) y paréntesis izquierdo
            
            if ((es_simbolo(actual) or actual == ')' or actual in '*+') and
                (es_simbolo(siguiente) or siguiente == '(')):
                resultado.append('.')
    
    return ''.join(resultado)

def es_simbolo(caracter):
    """
    Determina si un carácter es un símbolo del alfabeto
    (letras, dígitos o épsilon)
    """
    return (caracter.isalnum() or caracter == 'ε' or caracter == 'E')

def mostrar_conversion(expresion):
    """
    Muestra el proceso de conversión de infix a postfix
    """
    print(f"Expresión original: {expresion}")
    expresion_con_concat = agregar_concatenacion(expresion)
    print(f"Con concatenación explícita: {expresion_con_concat}")
    resultado = convertir_a_postfix(expresion)
    print(f"Notación postfix: {resultado}")
    return resultado
