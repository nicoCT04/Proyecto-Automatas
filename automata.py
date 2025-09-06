"""
Clase principal para representar autómatas finitos
"""
import json
from typing import Set, Dict, List, Tuple, Optional

class Automata:
    def __init__(self):
        self.estados = set()
        self.simbolos = set()
        self.estado_inicial = None
        self.estados_aceptacion = set()
        self.transiciones = {}  # {(estado_origen, simbolo): {estado_destino}}
        
    def agregar_estado(self, estado):
        """Agrega un estado al autómata"""
        self.estados.add(estado)
        
    def agregar_simbolo(self, simbolo):
        """Agrega un símbolo al alfabeto"""
        self.simbolos.add(simbolo)
        
    def establecer_estado_inicial(self, estado):
        """Establece el estado inicial"""
        self.estado_inicial = estado
        self.agregar_estado(estado)
        
    def agregar_estado_aceptacion(self, estado):
        """Agrega un estado de aceptación"""
        self.estados_aceptacion.add(estado)
        self.agregar_estado(estado)
        
    def agregar_transicion(self, estado_origen, simbolo, estado_destino):
        """Agrega una transición al autómata"""
        self.agregar_estado(estado_origen)
        self.agregar_estado(estado_destino)
        if simbolo != 'ε':  # No agregar épsilon al alfabeto
            self.agregar_simbolo(simbolo)
            
        clave = (estado_origen, simbolo)
        if clave not in self.transiciones:
            self.transiciones[clave] = set()
        self.transiciones[clave].add(estado_destino)
        
    def obtener_transiciones(self, estado, simbolo):
        """Obtiene los estados destino para una transición"""
        clave = (estado, simbolo)
        return self.transiciones.get(clave, set())
        
    def guardar_archivo(self, nombre_archivo):
        """Guarda el autómata en un archivo JSON"""
        datos = {
            'ESTADOS': sorted(list(self.estados)),
            'SIMBOLOS': sorted(list(self.simbolos)),
            'INICIO': self.estado_inicial,
            'ACEPTACION': sorted(list(self.estados_aceptacion)),
            'TRANSICIONES': []
        }
        
        for (estado_origen, simbolo), estados_destino in self.transiciones.items():
            for estado_destino in estados_destino:
                datos['TRANSICIONES'].append([estado_origen, simbolo, estado_destino])
        
        datos['TRANSICIONES'].sort()
        
        with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
            json.dump(datos, archivo, indent=2, ensure_ascii=False)
            
    def mostrar_info(self):
        """Muestra información básica del autómata"""
        print(f"Estados: {sorted(self.estados)}")
        print(f"Símbolos: {sorted(self.simbolos)}")
        print(f"Estado inicial: {self.estado_inicial}")
        print(f"Estados de aceptación: {sorted(self.estados_aceptacion)}")
        print("Transiciones:")
        for (estado_origen, simbolo), estados_destino in sorted(self.transiciones.items()):
            for estado_destino in sorted(estados_destino):
                print(f"  ({estado_origen}, {simbolo}) -> {estado_destino}")
