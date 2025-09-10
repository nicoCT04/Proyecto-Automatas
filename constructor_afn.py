"""
Implementación del algoritmo de Thompson para convertir expresiones regulares a AFN
"""
from automata import Automata

class ConstructorAFN:
    def __init__(self):
        self.contador_estados = 0
        
    def nuevo_estado(self):
        """Genera un nuevo estado único"""
        estado = self.contador_estados
        self.contador_estados += 1
        return estado
        
    def convertir_postfix_a_afn(self, postfix):
        """
        Convierte una expresión en notación postfix a un AFN usando el algoritmo de Thompson
        """
        pila = []
        
        for simbolo in postfix:
            if simbolo == '·':
                # Concatenación
                if len(pila) >= 2:
                    afn2 = pila.pop()
                    afn1 = pila.pop()
                    afn_concatenado = self.concatenar(afn1, afn2)
                    pila.append(afn_concatenado)
            elif simbolo == '|':
                # Unión
                if len(pila) >= 2:
                    afn2 = pila.pop()
                    afn1 = pila.pop()
                    afn_union = self.union(afn1, afn2)
                    pila.append(afn_union)
            elif simbolo == '*':
                # Estrella de Kleene
                if len(pila) >= 1:
                    afn = pila.pop()
                    afn_estrella = self.estrella_kleene(afn)
                    pila.append(afn_estrella)
            elif simbolo == '+':
                # Positiva (una o más repeticiones)
                if len(pila) >= 1:
                    afn = pila.pop()
                    afn_positiva = self.positiva(afn)
                    pila.append(afn_positiva)
            elif simbolo == '?':
                # Opcional (cero o una repetición)
                if len(pila) >= 1:
                    afn = pila.pop()
                    afn_opcional = self.opcional(afn)
                    pila.append(afn_opcional)
            elif self.es_simbolo(simbolo):
                # Crear AFN básico para un símbolo (verificar DESPUÉS de operadores)
                afn = self.crear_afn_simbolo(simbolo)
                pila.append(afn)
        
        if pila:
            return pila[0]
        else:
            # AFN vacío
            return self.crear_afn_vacio()
    
    def es_simbolo(self, caracter):
        """
        Determina si un carácter es un símbolo del alfabeto
        (letras, dígitos, épsilon, @, . literal, etc.)
        """
        # Operadores y metacaracteres reservados del regex  
        operadores_reservados = {'|', '·', '*', '+', '(', ')', '[', ']', '\\', '?'}
        
        # Un símbolo es cualquier carácter que NO sea un operador reservado
        # El punto (.) es ahora un símbolo literal
        # El operador de concatenación es · (MIDDLE DOT)
        return caracter not in operadores_reservados
    
    def crear_afn_simbolo(self, simbolo):
        """Crea un AFN básico que acepta un solo símbolo"""
        afn = Automata()
        estado_inicial = self.nuevo_estado()
        estado_final = self.nuevo_estado()
        
        afn.establecer_estado_inicial(estado_inicial)
        afn.agregar_estado_aceptacion(estado_final)
        
        if simbolo == 'ε' or simbolo == 'E':
            # Para épsilon, hacer transición épsilon
            afn.agregar_transicion(estado_inicial, 'ε', estado_final)
        elif simbolo == '●':
            # Punto literal - convertir de vuelta a '.'
            afn.agregar_transicion(estado_inicial, '.', estado_final)
        elif simbolo == '◆':
            # Signo de interrogación literal - convertir de vuelta a '?'
            afn.agregar_transicion(estado_inicial, '?', estado_final)
        elif simbolo == '◎':
            # Paréntesis izquierdo literal - convertir de vuelta a '('
            afn.agregar_transicion(estado_inicial, '(', estado_final)
        elif simbolo == '◉':
            # Paréntesis derecho literal - convertir de vuelta a ')'
            afn.agregar_transicion(estado_inicial, ')', estado_final)
        elif simbolo == '◈':
            # Barra invertida literal - convertir de vuelta a '\'
            afn.agregar_transicion(estado_inicial, '\\', estado_final)
        elif simbolo == '◊':
            # Llave izquierda literal - convertir de vuelta a '{'
            afn.agregar_transicion(estado_inicial, '{', estado_final)
        elif simbolo == '◘':
            # Llave derecha literal - convertir de vuelta a '}'
            afn.agregar_transicion(estado_inicial, '}', estado_final)
        else:
            afn.agregar_transicion(estado_inicial, simbolo, estado_final)
        
        return afn
    
    def crear_afn_vacio(self):
        """Crea un AFN que no acepta nada"""
        afn = Automata()
        estado = self.nuevo_estado()
        afn.establecer_estado_inicial(estado)
        return afn
    
    def concatenar(self, afn1, afn2):
        """Concatena dos AFN"""
        afn_resultado = Automata()
        
        # Copiar todos los estados y transiciones de ambos AFN
        afn_resultado.estados = afn1.estados.union(afn2.estados)
        afn_resultado.simbolos = afn1.simbolos.union(afn2.simbolos)
        afn_resultado.estado_inicial = afn1.estado_inicial
        afn_resultado.estados_aceptacion = afn2.estados_aceptacion.copy()
        afn_resultado.transiciones = {**afn1.transiciones, **afn2.transiciones}
        
        # Conectar estados finales de afn1 con estado inicial de afn2 mediante épsilon
        for estado_final in afn1.estados_aceptacion:
            afn_resultado.agregar_transicion(estado_final, 'ε', afn2.estado_inicial)
        
        return afn_resultado
    
    def union(self, afn1, afn2):
        """Crea la unión de dos AFN"""
        afn_resultado = Automata()
        
        # Nuevo estado inicial
        nuevo_inicial = self.nuevo_estado()
        afn_resultado.establecer_estado_inicial(nuevo_inicial)
        
        # Nuevo estado final
        nuevo_final = self.nuevo_estado()
        afn_resultado.agregar_estado_aceptacion(nuevo_final)
        
        # Copiar estados y transiciones de ambos AFN
        afn_resultado.estados = afn_resultado.estados.union(afn1.estados).union(afn2.estados)
        afn_resultado.simbolos = afn1.simbolos.union(afn2.simbolos)
        afn_resultado.transiciones = {**afn1.transiciones, **afn2.transiciones}
        
        # Conectar nuevo inicial con iniciales de ambos AFN
        afn_resultado.agregar_transicion(nuevo_inicial, 'ε', afn1.estado_inicial)
        afn_resultado.agregar_transicion(nuevo_inicial, 'ε', afn2.estado_inicial)
        
        # Conectar estados finales de ambos AFN con nuevo final
        for estado_final in afn1.estados_aceptacion:
            afn_resultado.agregar_transicion(estado_final, 'ε', nuevo_final)
        for estado_final in afn2.estados_aceptacion:
            afn_resultado.agregar_transicion(estado_final, 'ε', nuevo_final)
        
        return afn_resultado
    
    def estrella_kleene(self, afn):
        """Aplica la estrella de Kleene a un AFN"""
        afn_resultado = Automata()
        
        # Nuevo estado inicial/final
        nuevo_estado = self.nuevo_estado()
        afn_resultado.establecer_estado_inicial(nuevo_estado)
        afn_resultado.agregar_estado_aceptacion(nuevo_estado)
        
        # Copiar estados y transiciones del AFN original
        afn_resultado.estados = afn_resultado.estados.union(afn.estados)
        afn_resultado.simbolos = afn.simbolos.copy()
        afn_resultado.transiciones = afn.transiciones.copy()
        
        # Conectar nuevo estado con el inicial del AFN original
        afn_resultado.agregar_transicion(nuevo_estado, 'ε', afn.estado_inicial)
        
        # Conectar estados finales del AFN original con su inicial y con el nuevo estado
        for estado_final in afn.estados_aceptacion:
            afn_resultado.agregar_transicion(estado_final, 'ε', afn.estado_inicial)
            afn_resultado.agregar_transicion(estado_final, 'ε', nuevo_estado)
        
        return afn_resultado
    
    def positiva(self, afn):
        """Aplica el operador + (una o más repeticiones) a un AFN"""
        afn_resultado = Automata()
        
        # Nuevo estado final
        nuevo_final = self.nuevo_estado()
        afn_resultado.agregar_estado_aceptacion(nuevo_final)
        
        # Copiar estados y transiciones del AFN original
        afn_resultado.estados = afn.estados.copy()
        afn_resultado.estados.add(nuevo_final)
        afn_resultado.simbolos = afn.simbolos.copy()
        afn_resultado.estado_inicial = afn.estado_inicial
        afn_resultado.transiciones = afn.transiciones.copy()
        
        # Conectar estados finales del AFN original con el nuevo final y con el inicial
        for estado_final in afn.estados_aceptacion:
            afn_resultado.agregar_transicion(estado_final, 'ε', nuevo_final)
            afn_resultado.agregar_transicion(estado_final, 'ε', afn.estado_inicial)
        
        return afn_resultado
    
    def opcional(self, afn):
        """Aplica el operador ? (cero o una repetición) a un AFN"""
        afn_resultado = Automata()
        
        # Nuevo estado inicial/final
        nuevo_estado = self.nuevo_estado()
        afn_resultado.establecer_estado_inicial(nuevo_estado)
        afn_resultado.agregar_estado_aceptacion(nuevo_estado)
        
        # Copiar estados y transiciones del AFN original
        afn_resultado.estados = afn_resultado.estados.union(afn.estados)
        afn_resultado.simbolos = afn.simbolos.copy()
        afn_resultado.transiciones = afn.transiciones.copy()
        
        # Conectar nuevo estado con el inicial del AFN original (para "una ocurrencia")
        afn_resultado.agregar_transicion(nuevo_estado, 'ε', afn.estado_inicial)
        
        # Conectar estados finales del AFN original con el nuevo estado final
        for estado_final in afn.estados_aceptacion:
            afn_resultado.agregar_transicion(estado_final, 'ε', nuevo_estado)
        
        # El nuevo estado ya es de aceptación, permitiendo "cero ocurrencias"
        return afn_resultado
