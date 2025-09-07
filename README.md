# Proyecto de Teoría de la Computación

Este proyecto implementa los algoritmos fundamentales para la construcción y minimización de autómatas finitos a partir de expresiones regulares.

## Características Implementadas

- ✅ **Algoritmo Shunting Yard**: Conversión de expresiones regulares a notación postfix
- ✅ **Algoritmo de Thompson**: Conversión de expresiones regulares a AFN (Autómata Finito No-determinista)
- ✅ **Construcción de Subconjuntos**: Conversión de AFN a AFD (Autómata Finito Determinista)
- ✅ **Algoritmo de Hopcroft**: Minimización de AFD
- ✅ **Simulador de AFD**: Prueba de cadenas en el autómata final
- ✅ **Visualización**: Generación de archivos DOT y diagramas gráficos

## Estructura del Proyecto

```
Proyecto1/
├── main.py                 # Programa principal
├── automata.py            # Clase base para autómatas
├── shunting_yard.py       # Conversión infix a postfix
├── constructor_afn.py     # Algoritmo de Thompson
├── constructor_afd.py     # Construcción de subconjuntos
├── minimizador_afd.py     # Algoritmo de Hopcroft
├── simulador_afd.py       # Simulación de cadenas
├── visualizador.py        # Generación de visualizaciones
└── README.md             # Este archivo
```

## Uso del Programa

### Ejecución

```bash
python3 main.py
```

### Operadores Soportados

- `|` : Unión (OR)
- `*` : Estrella de Kleene (cero o más repeticiones)
- `+` : Positiva (una o más repeticiones)
- `()` : Agrupación
- Concatenación implícita

### Símbolos del Alfabeto

- Letras minúsculas y mayúsculas (a-z, A-Z)
- Dígitos (0-9)
- `ε` : Cadena vacía (también se puede usar `E`)

### Ejemplos de Expresiones Regulares

1. `(a|b)*abb` - Cadenas que terminan en "abb"
2. `a*b+` - Cero o más 'a' seguidas de una o más 'b'
3. `(a|b)*` - Cualquier cadena de 'a' y 'b'
4. `ab*a` - 'a' seguida de cero o más 'b' y otra 'a'

## Archivos Generados

Para cada expresión regular procesada, el programa genera archivos organizados en carpetas específicas. **Los archivos de expresiones anteriores se sobrescriben automáticamente**, manteniendo siempre solo los resultados de la última expresión procesada.


**📝 Nota**: Cada vez que ejecutes el programa con una nueva expresión, se limpian automáticamente las carpetas y se generan nuevos archivos, manteniendo solo los resultados de la última expresión procesada.

### Tipos de Archivos Generados

#### Archivos de Visualización
- **DOT**: Código GraphViz para visualización
- **PNG**: Imagen del diagrama del autómata
- **TXT**: Descripción textual legible

### Formato de Archivos JSON

```json
{
  "ESTADOS": [0, 1, 2, 3],
  "SIMBOLOS": ["a", "b"],
  "INICIO": 0,
  "ACEPTACION": [3],
  "TRANSICIONES": [
    [0, "a", 1],
    [1, "b", 2],
    [2, "b", 3]
  ]
}
```

## Instalación de Dependencias

### GraphViz (para visualizaciones)

**macOS:**
```bash
brew install graphviz
```

**Ubuntu/Debian:**
```bash
sudo apt-get install graphviz
```

**Windows:**
- Descargar desde [graphviz.org](https://graphviz.org/download/)
- O con Chocolatey: `choco install graphviz`

### Alternativas para Visualización

Si no tienes GraphViz instalado, puedes:
1. Usar los archivos `.dot` en [GraphViz Online](https://dreampuf.github.io/GraphvizOnline/)
2. Instalar la extensión "Graphviz Preview" en VS Code
3. Usar [edotor.net](https://edotor.net/)

## Ejemplo de Uso Completo

```
PROCESANDO EXPRESIÓN REGULAR: (a|b)*abb

1. CONVERSIÓN A NOTACIÓN POSTFIX
----------------------------------------
Expresión original: (a|b)*abb
Con concatenación explícita: (a|b)*.a.b.b
Notación postfix: ab|*a.b.b.

2. CONSTRUCCIÓN DE AFN (Thompson)
----------------------------------------
AFN Generado
============
Estados: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
Alfabeto: ['a', 'b']
Estado inicial: 0
Estados de aceptación: [10]

3. CONVERSIÓN AFN A AFD (Construcción de Subconjuntos)
----------------------------------------
AFD Generado
============
Estados: [0, 1, 2, 3]
Alfabeto: ['a', 'b']
Estado inicial: 0
Estados de aceptación: [3]

4. MINIMIZACIÓN DEL AFD (Hopcroft)
----------------------------------------
AFD Minimizado
==============
Estados: [0, 1, 2, 3]
Alfabeto: ['a', 'b']
Estado inicial: 0
Estados de aceptación: [3]
```

## Simulación de Cadenas

El programa permite probar cadenas en el AFD minimizado:

```
Alfabeto del autómata: ['a', 'b']
Ingresa una cadena para probar: abb

Simulando cadena: 'abb'
--------------------------------------------------
Estado inicial: 0

Paso 1: Procesando símbolo 'a'
Estado actual: 0
Transición: (0, a) -> 1

Paso 2: Procesando símbolo 'b'
Estado actual: 1
Transición: (1, b) -> 2

Paso 3: Procesando símbolo 'b'
Estado actual: 2
Transición: (2, b) -> 3

Estado final: 3
Estados de aceptación: [3]
Cadena ACEPTADA ✓
```

## Algoritmos Implementados

### 1. Shunting Yard
- Convierte expresiones regulares de notación infija a postfija
- Maneja precedencia de operadores correctamente
- Agrega concatenación explícita donde es necesaria

### 2. Thompson (AFN)
- Construye AFN usando operaciones básicas:
  - Símbolo individual
  - Concatenación
  - Unión
  - Estrella de Kleene
  - Operador positivo

### 3. Construcción de Subconjuntos (AFD)
- Elimina no-determinismo
- Calcula epsilon-clausuras
- Genera tabla de transiciones determinista

### 4. Hopcroft (Minimización)
- Elimina estados inalcanzables
- Particiona estados equivalentes
- Genera AFD con número mínimo de estados

## Características Adicionales

- **Interfaz amigable**: Menús claros y proceso paso a paso
- **Validación de entrada**: Verifica símbolos válidos en las cadenas
- **Múltiples formatos**: JSON, texto plano, GraphViz
- **Visualización interactiva**: Tabla de transiciones y simulación paso a paso
- **Manejo de errores**: Mensajes informativos para problemas comunes

## Autores

Proyecto desarrollado para el curso de Teoría de la Computación 2025.
