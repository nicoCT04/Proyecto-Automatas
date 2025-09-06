"""
Implementación del algoritmo de Hopcroft para minimización de AFD
"""
from automata import Automata

class MinimizadorAFD:
    def minimizar_afd(self, afd):
        """
        Minimiza un AFD usando el algoritmo de Hopcroft
        """
        # Paso 1: Eliminar estados inalcanzables
        afd_alcanzable = self.eliminar_estados_inalcanzables(afd)
        
        # Paso 2: Crear partición inicial (estados de aceptación vs. no aceptación)
        particiones = self.crear_particion_inicial(afd_alcanzable)
        
        # Paso 3: Refinar particiones hasta que no haya más cambios
        particiones = self.refinar_particiones(afd_alcanzable, particiones)
        
        # Paso 4: Construir AFD minimizado
        return self.construir_afd_minimizado(afd_alcanzable, particiones)
    
    def eliminar_estados_inalcanzables(self, afd):
        """
        Elimina estados que no son alcanzables desde el estado inicial
        """
        estados_alcanzables = set()
        cola = [afd.estado_inicial]
        estados_alcanzables.add(afd.estado_inicial)
        
        while cola:
            estado_actual = cola.pop(0)
            
            for simbolo in afd.simbolos:
                estados_destino = afd.obtener_transiciones(estado_actual, simbolo)
                for estado_destino in estados_destino:
                    if estado_destino not in estados_alcanzables:
                        estados_alcanzables.add(estado_destino)
                        cola.append(estado_destino)
        
        # Crear nuevo AFD solo con estados alcanzables
        afd_alcanzable = Automata()
        afd_alcanzable.estados = estados_alcanzables
        afd_alcanzable.simbolos = afd.simbolos.copy()
        afd_alcanzable.estado_inicial = afd.estado_inicial
        afd_alcanzable.estados_aceptacion = afd.estados_aceptacion.intersection(estados_alcanzables)
        
        # Copiar transiciones relevantes
        for (estado_origen, simbolo), estados_destino in afd.transiciones.items():
            if estado_origen in estados_alcanzables:
                for estado_destino in estados_destino:
                    if estado_destino in estados_alcanzables:
                        afd_alcanzable.agregar_transicion(estado_origen, simbolo, estado_destino)
        
        return afd_alcanzable
    
    def crear_particion_inicial(self, afd):
        """
        Crea la partición inicial: estados de aceptación y no aceptación
        """
        estados_no_aceptacion = afd.estados - afd.estados_aceptacion
        
        particiones = []
        if estados_no_aceptacion:
            particiones.append(estados_no_aceptacion)
        if afd.estados_aceptacion:
            particiones.append(afd.estados_aceptacion)
        
        return particiones
    
    def refinar_particiones(self, afd, particiones):
        """
        Refina las particiones hasta que no haya más cambios
        """
        cambio = True
        
        while cambio:
            cambio = False
            nuevas_particiones = []
            
            for particion in particiones:
                # Intentar dividir esta partición
                subparticiones = self.dividir_particion(afd, particion, particiones)
                
                if len(subparticiones) > 1:
                    cambio = True
                    nuevas_particiones.extend(subparticiones)
                else:
                    nuevas_particiones.append(particion)
            
            particiones = nuevas_particiones
        
        return particiones
    
    def dividir_particion(self, afd, particion, todas_particiones):
        """
        Intenta dividir una partición basándose en las transiciones
        """
        if len(particion) <= 1:
            return [particion]
        
        # Crear grupos basados en el comportamiento de transiciones
        grupos = {}
        
        for estado in particion:
            # Crear "firma" del estado basada en sus transiciones
            firma = []
            for simbolo in sorted(afd.simbolos):
                estados_destino = afd.obtener_transiciones(estado, simbolo)
                if estados_destino:
                    estado_destino = next(iter(estados_destino))  # AFD tiene solo una transición por símbolo
                    # Encontrar a qué partición pertenece el estado destino
                    particion_destino = self.encontrar_particion(estado_destino, todas_particiones)
                    firma.append(particion_destino)
                else:
                    firma.append(None)
            
            firma_tuple = tuple(firma)
            if firma_tuple not in grupos:
                grupos[firma_tuple] = set()
            grupos[firma_tuple].add(estado)
        
        return list(grupos.values())
    
    def encontrar_particion(self, estado, particiones):
        """
        Encuentra el índice de la partición que contiene el estado dado
        """
        for i, particion in enumerate(particiones):
            if estado in particion:
                return i
        return -1
    
    def construir_afd_minimizado(self, afd, particiones):
        """
        Construye el AFD minimizado a partir de las particiones finales
        """
        afd_min = Automata()
        
        # Mapeo de estados originales a estados de partición
        mapeo_estados = {}
        for i, particion in enumerate(particiones):
            for estado in particion:
                mapeo_estados[estado] = i
        
        # Estados del AFD minimizado son los índices de las particiones
        afd_min.estados = set(range(len(particiones)))
        afd_min.simbolos = afd.simbolos.copy()
        
        # Estado inicial
        afd_min.estado_inicial = mapeo_estados[afd.estado_inicial]
        
        # Estados de aceptación
        for estado_aceptacion in afd.estados_aceptacion:
            estado_particion = mapeo_estados[estado_aceptacion]
            afd_min.agregar_estado_aceptacion(estado_particion)
        
        # Transiciones
        transiciones_agregadas = set()
        for (estado_origen, simbolo), estados_destino in afd.transiciones.items():
            estado_origen_min = mapeo_estados[estado_origen]
            for estado_destino in estados_destino:
                estado_destino_min = mapeo_estados[estado_destino]
                
                # Evitar duplicados
                if (estado_origen_min, simbolo, estado_destino_min) not in transiciones_agregadas:
                    afd_min.agregar_transicion(estado_origen_min, simbolo, estado_destino_min)
                    transiciones_agregadas.add((estado_origen_min, simbolo, estado_destino_min))
        
        return afd_min
