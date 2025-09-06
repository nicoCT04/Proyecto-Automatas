#!/usr/bin/env python3
"""
Programa principal para el proyecto de Teoría de la Computación
Convierte expresiones regulares a autómatas y los minimiza
"""

from shunting_yard import convertir_a_postfix, mostrar_conversion
from constructor_afn import ConstructorAFN
from constructor_afd import ConstructorAFD
from minimizador_afd import MinimizadorAFD
from simulador_afd import SimuladorAFD
from visualizador import (crear_visualizacion_graphviz, crear_visualizacion_simple, 
                         mostrar_automata_consola, instalar_graphviz_info, guardar_automata_completo, 
                         limpiar_y_crear_carpetas)

def procesar_expresion_regular(expresion):
    """
    Procesa una expresión regular completa: de regexp a AFD mínimo
    """
    print(f"\n{'='*60}")
    print(f"PROCESANDO EXPRESIÓN REGULAR: {expresion}")
    print(f"{'='*60}")
    
    # Limpiar y crear carpetas (solo mantiene archivos de la última expresión)
    print("\n📁 Preparando carpetas de resultados...")
    limpiar_y_crear_carpetas()
    print("✓ Carpetas limpias y listas para nuevos resultados")
    
    # Crear nombre base para archivos (sin caracteres especiales)
    nombre_base = expresion.replace('(', '').replace(')', '').replace('|', 'o').replace('*', 'estrella').replace('+', 'mas').replace(' ', '')
    
    # Paso 1: Convertir a notación postfix
    print("\n1. CONVERSIÓN A NOTACIÓN POSTFIX")
    print("-" * 40)
    postfix = mostrar_conversion(expresion)
    
    # Paso 2: Construir AFN
    print("\n2. CONSTRUCCIÓN DE AFN (Thompson)")
    print("-" * 40)
    constructor_afn = ConstructorAFN()
    afn = constructor_afn.convertir_postfix_a_afn(postfix)
    mostrar_automata_consola(afn, "AFN Generado")
    
    # Guardar AFN en carpeta específica
    guardar_automata_completo(afn, "afn_resultado", "AFN", f"AFN para: {expresion}")
    
    # Paso 3: Convertir AFN a AFD
    print("\n3. CONVERSIÓN AFN A AFD (Construcción de Subconjuntos)")
    print("-" * 40)
    constructor_afd = ConstructorAFD()
    afd = constructor_afd.convertir_afn_a_afd(afn)
    mostrar_automata_consola(afd, "AFD Generado")
    
    # Guardar AFD en carpeta específica
    guardar_automata_completo(afd, "afd_resultado", "AFD", f"AFD para: {expresion}")
    
    # Paso 4: Minimizar AFD
    print("\n4. MINIMIZACIÓN DEL AFD (Hopcroft)")
    print("-" * 40)
    minimizador = MinimizadorAFD()
    afd_min = minimizador.minimizar_afd(afd)
    mostrar_automata_consola(afd_min, "AFD Minimizado")
    
    # Guardar AFD minimizado en carpeta específica
    guardar_automata_completo(afd_min, "afd_min_resultado", "AFD_MIN", f"AFD Mínimo para: {expresion}")
    
    print(f"\n✓ Resultados guardados para: {expresion}")
    print("✓ Solo se mantienen los archivos de la última expresión procesada")
    
    return afd_min

def simular_cadenas(afd_min, expresion):
    """
    Permite al usuario probar cadenas en el AFD minimizado
    """
    simulador = SimuladorAFD(afd_min)
    
    print(f"\n{'='*60}")
    print(f"SIMULACIÓN DE CADENAS PARA: {expresion}")
    print(f"{'='*60}")
    
    # Mostrar información del autómata
    simulador.mostrar_tabla_transiciones()
    
    while True:
        print(f"\nAlbeto del autómata: {sorted(afd_min.simbolos)}")
        cadena = input("\nIngresa una cadena para probar (o 'salir' para terminar): ").strip()
        
        if cadena.lower() == 'salir':
            break
        
        if cadena == '':
            # Cadena vacía - usar epsilon
            print("Probando cadena vacía (ε)")
            # Para cadena vacía, verificar si el estado inicial es de aceptación
            if afd_min.estado_inicial in afd_min.estados_aceptacion:
                print("Cadena vacía ACEPTADA ✓")
            else:
                print("Cadena vacía RECHAZADA ✗")
        else:
            simulador.simular_cadena(cadena)

def mostrar_menu():
    """
    Muestra el menú principal
    """
    print(f"\n{'='*60}")
    print("PROYECTO TEORÍA DE LA COMPUTACIÓN")
    print("Conversión de Expresiones Regulares a Autómatas")
    print(f"{'='*60}")
    print("Este programa convierte expresiones regulares a AFN, AFD y AFD mínimo")
    print("Operadores soportados: | (unión), * (estrella), + (positiva), () (agrupación)")
    print("Símbolos: letras, números, ε (épsilon)")
    print()

def main():
    """
    Función principal del programa
    """
    mostrar_menu()
    instalar_graphviz_info()
    
    while True:
        print(f"\n{'-'*40}")
        expresion = input("Ingresa una expresión regular (o 'salir' para terminar): ").strip()
        
        if expresion.lower() == 'salir':
            print("¡Gracias por usar el programa!")
            break
        
        if not expresion:
            print("Por favor ingresa una expresión válida")
            continue
        
        try:
            # Procesar expresión regular
            afd_min = procesar_expresion_regular(expresion)
            
            # Preguntar si quiere simular cadenas
            while True:
                respuesta = input("\n¿Quieres probar cadenas en este autómata? (s/n): ").strip().lower()
                if respuesta in ['s', 'si', 'sí', 'y', 'yes']:
                    simular_cadenas(afd_min, expresion)
                    break
                elif respuesta in ['n', 'no']:
                    break
                else:
                    print("Por favor responde 's' o 'n'")
                    
        except Exception as e:
            print(f"Error al procesar la expresión: {e}")
            print("Verifica que la expresión esté bien formada")

if __name__ == "__main__":
    main()
