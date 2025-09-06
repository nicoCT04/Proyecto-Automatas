"""
Visualizador de autómatas usando graphviz
"""
import os

def limpiar_y_crear_carpetas():
    """
    Limpia y crea las carpetas para organizar los resultados
    Solo mantiene los archivos de la última expresión procesada
    """
    carpetas = [
        "Resultados_AFN",
        "Resultados_AFD", 
        "Resultados_AFD_Minimo"
    ]
    
    for carpeta in carpetas:
        # Si la carpeta existe, limpiar su contenido
        if os.path.exists(carpeta):
            for archivo in os.listdir(carpeta):
                ruta_archivo = os.path.join(carpeta, archivo)
                if os.path.isfile(ruta_archivo):
                    os.remove(ruta_archivo)
        else:
            # Si no existe, crearla
            os.makedirs(carpeta)
        
    return carpetas
        
def guardar_automata_completo(automata, nombre_base, tipo_automata, titulo):
    """
    Guarda un autómata completo (JSON, DOT, PNG, TXT) en la carpeta apropiada
    """
    # Determinar carpeta según el tipo
    carpetas_map = {
        "AFN": "Resultados_AFN",
        "AFD": "Resultados_AFD", 
        "AFD_MIN": "Resultados_AFD_Minimo"
    }
    
    carpeta = carpetas_map.get(tipo_automata, ".")
    
    # Crear carpeta si no existe
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)
    
    # Rutas completas para los archivos
    ruta_base = os.path.join(carpeta, nombre_base)
    
    # Guardar JSON
    automata.guardar_archivo(f"{ruta_base}.json")
    
    # Guardar visualización simple
    crear_visualizacion_simple(automata, ruta_base)
    
    # Guardar visualización graphviz
    crear_visualizacion_graphviz(automata, ruta_base, titulo)
    
    print(f"✓ Archivos guardados en {carpeta}:")
    print(f"  - {nombre_base}.json (descripción formal)")
    print(f"  - {nombre_base}.png (diagrama)")
    print(f"  - {nombre_base}.dot (código graphviz)")
    print(f"  - {nombre_base}.txt (descripción textual)")
    
    return ruta_base

def crear_visualizacion_graphviz(automata, nombre_archivo, titulo="Autómata"):
    """
    Crea una visualización del autómata usando graphviz
    """
    contenido_dot = generar_codigo_dot(automata, titulo)
    
    # Guardar archivo .dot
    archivo_dot = f"{nombre_archivo}.dot"
    with open(archivo_dot, 'w', encoding='utf-8') as f:
        f.write(contenido_dot)
    
    print(f"Archivo DOT generado: {archivo_dot}")
    
    try:
        # Intentar generar imagen PNG
        comando_png = f"dot -Tpng {archivo_dot} -o {nombre_archivo}.png"
        resultado = os.system(comando_png)
        
        if resultado == 0:
            print(f"Imagen PNG generada: {nombre_archivo}.png")
        else:
            print("No se pudo generar la imagen PNG. Asegúrate de tener Graphviz instalado.")
            print("Puedes instalar Graphviz desde: https://graphviz.org/download/")
            
    except Exception as e:
        print(f"Error al generar imágenes: {e}")
        print("El archivo .dot se puede abrir con herramientas compatibles con Graphviz")

def generar_codigo_dot(automata, titulo):
    """
    Genera el código DOT para representar el autómata
    """
    dot = []
    dot.append("digraph automata {")
    dot.append("    rankdir=LR;")
    dot.append("    size=\"8,5\";")
    dot.append(f"    label=\"{titulo}\";")
    dot.append("    labelloc=\"t\";")
    dot.append("    node [shape = circle];")
    dot.append("")
    
    # Estados de aceptación (círculo doble)
    if automata.estados_aceptacion:
        estados_aceptacion_str = " ".join([f'"{estado}"' for estado in sorted(automata.estados_aceptacion)])
        dot.append(f"    node [shape = doublecircle]; {estados_aceptacion_str};")
        dot.append("")
    
    # Estado inicial (flecha desde punto invisible)
    dot.append("    node [shape = circle];")
    dot.append(f"    start [shape=point, width=0];")
    dot.append(f"    start -> \"{automata.estado_inicial}\";")
    dot.append("")
    
    # Agrupar transiciones por origen y destino para evitar múltiples flechas
    transiciones_agrupadas = {}
    
    for (estado_origen, simbolo), estados_destino in automata.transiciones.items():
        for estado_destino in estados_destino:
            clave = (estado_origen, estado_destino)
            if clave not in transiciones_agrupadas:
                transiciones_agrupadas[clave] = []
            transiciones_agrupadas[clave].append(simbolo)
    
    # Generar transiciones
    for (estado_origen, estado_destino), simbolos in transiciones_agrupadas.items():
        simbolos_ordenados = sorted(simbolos)
        etiqueta = ", ".join(simbolos_ordenados)
        
        # Reemplazar épsilon con símbolo unicode
        etiqueta = etiqueta.replace('ε', 'ε').replace('E', 'ε')
        
        dot.append(f"    \"{estado_origen}\" -> \"{estado_destino}\" [label=\"{etiqueta}\"];")
    
    dot.append("}")
    
    return "\n".join(dot)

def crear_visualizacion_simple(automata, nombre_archivo):
    """
    Crea una representación textual simple del autómata
    """
    contenido = []
    contenido.append(f"Autómata: {nombre_archivo}")
    contenido.append("=" * 50)
    contenido.append("")
    
    contenido.append(f"Estados: {{{', '.join(map(str, sorted(automata.estados)))}}}")
    contenido.append(f"Alfabeto: {{{', '.join(sorted(automata.simbolos))}}}")
    contenido.append(f"Estado inicial: {automata.estado_inicial}")
    contenido.append(f"Estados de aceptación: {{{', '.join(map(str, sorted(automata.estados_aceptacion)))}}}")
    contenido.append("")
    
    contenido.append("Transiciones:")
    for (estado_origen, simbolo), estados_destino in sorted(automata.transiciones.items()):
        for estado_destino in sorted(estados_destino):
            contenido.append(f"  δ({estado_origen}, {simbolo}) = {estado_destino}")
    
    # Guardar en archivo de texto
    archivo_txt = f"{nombre_archivo}.txt"
    with open(archivo_txt, 'w', encoding='utf-8') as f:
        f.write("\n".join(contenido))
    
    print(f"Descripción textual guardada: {archivo_txt}")

def mostrar_automata_consola(automata, titulo):
    """
    Muestra el autómata en la consola de forma organizada
    """
    print(f"\n{titulo}")
    print("=" * len(titulo))
    print(f"Estados: {sorted(automata.estados)}")
    print(f"Alfabeto: {sorted(automata.simbolos)}")
    print(f"Estado inicial: {automata.estado_inicial}")
    print(f"Estados de aceptación: {sorted(automata.estados_aceptacion)}")
    print("\nTransiciones:")
    
    if not automata.transiciones:
        print("  (ninguna)")
    else:
        for (estado_origen, simbolo), estados_destino in sorted(automata.transiciones.items()):
            for estado_destino in sorted(estados_destino):
                print(f"  δ({estado_origen}, {simbolo}) = {estado_destino}")
    print()

def instalar_graphviz_info():
    """
    Muestra información sobre cómo instalar Graphviz
    """
    print("\nPara generar las visualizaciones gráficas, necesitas instalar Graphviz:")
    print("\nmacOS (con Homebrew):")
    print("  brew install graphviz")
    print("\nUbuntu/Debian:")
    print("  sudo apt-get install graphviz")
    print("\nWindows:")
    print("  Descarga desde https://graphviz.org/download/")
    print("  O con chocolatey: choco install graphviz")
    print("\nTambién puedes visualizar los archivos .dot en:")
    print("  - https://dreampuf.github.io/GraphvizOnline/")
    print("  - https://edotor.net/")
    print("  - VS Code con la extensión 'Graphviz Preview'")
