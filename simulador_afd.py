"""
Simulador para probar cadenas en un AFD
"""

class SimuladorAFD:
    def __init__(self, afd):
        self.afd = afd
        
    def simular_cadena(self, cadena):
        """
        Simula la ejecución de una cadena en el AFD
        Retorna True si la cadena es aceptada, False si no
        """
        print(f"\nSimulando cadena: '{cadena}'")
        print("-" * 50)
        
        estado_actual = self.afd.estado_inicial
        print(f"Estado inicial: {estado_actual}")
        
        # Verificar que todos los símbolos están en el alfabeto
        for simbolo in cadena:
            if simbolo not in self.afd.simbolos:
                print(f"Error: El símbolo '{simbolo}' no está en el alfabeto del autómata")
                print(f"Alfabeto: {sorted(self.afd.simbolos)}")
                return False
        
        # Procesar cada símbolo de la cadena
        for i, simbolo in enumerate(cadena):
            print(f"\nPaso {i+1}: Procesando símbolo '{simbolo}'")
            print(f"Estado actual: {estado_actual}")
            
            # Buscar transición
            estados_destino = self.afd.obtener_transiciones(estado_actual, simbolo)
            
            if not estados_destino:
                print(f"No hay transición desde el estado {estado_actual} con símbolo '{simbolo}'")
                print("Cadena RECHAZADA")
                return False
            
            # En un AFD solo debe haber una transición por símbolo
            estado_siguiente = next(iter(estados_destino))
            print(f"Transición: ({estado_actual}, {simbolo}) -> {estado_siguiente}")
            estado_actual = estado_siguiente
        
        # Verificar si el estado final es de aceptación
        print(f"\nEstado final: {estado_actual}")
        print(f"Estados de aceptación: {sorted(self.afd.estados_aceptacion)}")
        
        if estado_actual in self.afd.estados_aceptacion:
            print("Cadena ACEPTADA ✓")
            return True
        else:
            print("Cadena RECHAZADA ✗")
            return False
    
    def simular_cadena_paso_a_paso(self, cadena):
        """
        Simula una cadena paso a paso, mostrando cada transición
        """
        configuraciones = []
        estado_actual = self.afd.estado_inicial
        
        # Configuración inicial
        configuraciones.append((estado_actual, cadena, 0))
        
        for i, simbolo in enumerate(cadena):
            estados_destino = self.afd.obtener_transiciones(estado_actual, simbolo)
            
            if not estados_destino:
                configuraciones.append((None, cadena[i+1:], i+1))
                break
            
            estado_actual = next(iter(estados_destino))
            configuraciones.append((estado_actual, cadena[i+1:], i+1))
        
        return configuraciones, estado_actual in self.afd.estados_aceptacion
    
    def mostrar_tabla_transiciones(self):
        """
        Muestra la tabla de transiciones del AFD de forma organizada
        """
        print("\nTabla de transiciones:")
        print("-" * 50)
        
        simbolos_ordenados = sorted(self.afd.simbolos)
        estados_ordenados = sorted(self.afd.estados)
        
        # Encabezado
        print(f"{'Estado':<8}", end="")
        for simbolo in simbolos_ordenados:
            print(f"{simbolo:<8}", end="")
        print()
        
        print("-" * (8 + len(simbolos_ordenados) * 8))
        
        # Filas de la tabla
        for estado in estados_ordenados:
            # Marcar estado inicial y de aceptación
            marcador = ""
            if estado == self.afd.estado_inicial:
                marcador += "→"
            if estado in self.afd.estados_aceptacion:
                marcador += "*"
            
            print(f"{estado}{marcador:<7}", end="")
            
            for simbolo in simbolos_ordenados:
                estados_destino = self.afd.obtener_transiciones(estado, simbolo)
                if estados_destino:
                    destino = next(iter(estados_destino))
                    print(f"{destino:<8}", end="")
                else:
                    print(f"{'∅':<8}", end="")
            print()
        
        print("\nLeyenda: → estado inicial, * estado de aceptación")
    
    def probar_multiples_cadenas(self, cadenas):
        """
        Prueba múltiples cadenas y muestra un resumen
        """
        print("\nProbando múltiples cadenas:")
        print("=" * 60)
        
        resultados = []
        for cadena in cadenas:
            aceptada = self.simular_cadena(cadena)
            resultados.append((cadena, aceptada))
            print()
        
        print("Resumen de resultados:")
        print("-" * 30)
        for cadena, aceptada in resultados:
            estado = "ACEPTADA" if aceptada else "RECHAZADA"
            print(f"'{cadena}' -> {estado}")
        
        return resultados
