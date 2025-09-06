"""
Implementación del algoritmo de construcción de subconjuntos para convertir AFN a AFD
"""
from automata import Automata

class ConstructorAFD:
    def __init__(self):
        self.contador_estados = 0
        
    def convertir_afn_a_afd(self, afn):
        """
        Convierte un AFN a AFD usando el algoritmo de construcción de subconjuntos
        """
        afd = Automata()
        
        # Calcular epsilon-clausura del estado inicial
        epsilon_clausura_inicial = self.epsilon_clausura(afn, {afn.estado_inicial})
        
        # Estados del AFD son subconjuntos de estados del AFN
        # Usamos tuplas ordenadas para representar subconjuntos
        estado_inicial_afd = tuple(sorted(epsilon_clausura_inicial))
        afd.establecer_estado_inicial(estado_inicial_afd)
        
        # Cola de estados por procesar
        estados_por_procesar = [estado_inicial_afd]
        estados_procesados = set()
        
        # Mapeo de subconjuntos de AFN a estados de AFD
        mapeo_estados = {estado_inicial_afd: estado_inicial_afd}
        
        while estados_por_procesar:
            estado_actual = estados_por_procesar.pop(0)
            
            if estado_actual in estados_procesados:
                continue
                
            estados_procesados.add(estado_actual)
            
            # Verificar si es estado de aceptación
            conjunto_estados_afn = set(estado_actual)
            if conjunto_estados_afn.intersection(afn.estados_aceptacion):
                afd.agregar_estado_aceptacion(estado_actual)
            
            # Para cada símbolo del alfabeto
            for simbolo in afn.simbolos:
                # Calcular el conjunto destino
                conjunto_destino = set()
                for estado_afn in conjunto_estados_afn:
                    destinos = afn.obtener_transiciones(estado_afn, simbolo)
                    conjunto_destino.update(destinos)
                
                if conjunto_destino:
                    # Calcular epsilon-clausura del conjunto destino
                    epsilon_clausura_destino = self.epsilon_clausura(afn, conjunto_destino)
                    estado_destino_afd = tuple(sorted(epsilon_clausura_destino))
                    
                    # Agregar transición al AFD
                    afd.agregar_transicion(estado_actual, simbolo, estado_destino_afd)
                    
                    # Si es un nuevo estado, agregarlo a la cola
                    if estado_destino_afd not in estados_procesados:
                        estados_por_procesar.append(estado_destino_afd)
                        mapeo_estados[estado_destino_afd] = estado_destino_afd
        
        # Renumerar estados para mejor legibilidad
        return self.renumerar_estados(afd)
    
    def epsilon_clausura(self, afn, conjunto_estados):
        """
        Calcula la epsilon-clausura de un conjunto de estados
        """
        clausura = conjunto_estados.copy()
        pila = list(conjunto_estados)
        
        while pila:
            estado = pila.pop()
            # Buscar transiciones épsilon
            transiciones_epsilon = afn.obtener_transiciones(estado, 'ε')
            
            for estado_destino in transiciones_epsilon:
                if estado_destino not in clausura:
                    clausura.add(estado_destino)
                    pila.append(estado_destino)
        
        return clausura
    
    def renumerar_estados(self, afd):
        """
        Renumera los estados del AFD para tener nombres más simples
        """
        afd_renumerado = Automata()
        
        # Crear mapeo de estados antiguos a nuevos
        estados_ordenados = sorted(afd.estados, key=lambda x: (len(str(x)), str(x)))
        mapeo = {}
        for i, estado_viejo in enumerate(estados_ordenados):
            mapeo[estado_viejo] = i
        
        # Crear AFD renumerado
        afd_renumerado.estados = set(range(len(estados_ordenados)))
        afd_renumerado.simbolos = afd.simbolos.copy()
        afd_renumerado.estado_inicial = mapeo[afd.estado_inicial]
        
        # Renumerar estados de aceptación
        for estado_aceptacion in afd.estados_aceptacion:
            afd_renumerado.agregar_estado_aceptacion(mapeo[estado_aceptacion])
        
        # Renumerar transiciones
        for (estado_origen, simbolo), estados_destino in afd.transiciones.items():
            estado_origen_nuevo = mapeo[estado_origen]
            for estado_destino in estados_destino:
                estado_destino_nuevo = mapeo[estado_destino]
                afd_renumerado.agregar_transicion(estado_origen_nuevo, simbolo, estado_destino_nuevo)
        
        return afd_renumerado
