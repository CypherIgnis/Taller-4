import random
import time
import statistics
import matplotlib.pyplot as plt

from tallerAVL import ArbolAVL


TAMANOS = [
    1024,
    2048,
    4096,
    8192,
    16384,
    32768,
    65536,
]

REPETICIONES = 3
SEMILLA = 42


def medir_tiempos(n):

    tiempos_insercion = []
    tiempos_busqueda = []
    tiempos_eliminacion = []

    for repeticion in range(REPETICIONES):
        generador = random.Random(SEMILLA + repeticion)
        claves = list(range(n))
        generador.shuffle(claves)

        arbol = ArbolAVL()

        inicio = time.perf_counter()
        for clave in claves:
            arbol.insertar(clave)
        fin = time.perf_counter()

        tiempos_insercion.append(fin - inicio)

        inicio = time.perf_counter()
        for clave in claves:
            arbol.buscar(clave)
        fin = time.perf_counter()

        tiempos_busqueda.append(fin - inicio)

        arbol_eliminar = ArbolAVL()
        for clave in claves:
            arbol_eliminar.insertar(clave)

        inicio = time.perf_counter()
        for clave in claves:
            arbol_eliminar.eliminar(clave)
        fin = time.perf_counter()

        tiempos_eliminacion.append(fin - inicio)

    return (
        statistics.mean(tiempos_insercion),
        statistics.mean(tiempos_busqueda),
        statistics.mean(tiempos_eliminacion),
    )


def main():

    resultados = {
        "Inserción": [],
        "Búsqueda": [],
        "Eliminación": [],
    }

    print("PRUEBA DE TIEMPOS DEL ÁRBOL AVL")
    print(f"Repeticiones por tamaño: {REPETICIONES}")
    print("-" * 65)
    print(
        f"{'Nodos':>10} | {'Inserción (s)':>15} | "
        f"{'Búsqueda (s)':>15} | {'Eliminación (s)':>15}"
    )
    print("-" * 65)

    for n in TAMANOS:
        insercion, busqueda, eliminacion = medir_tiempos(n)

        resultados["Inserción"].append(insercion)
        resultados["Búsqueda"].append(busqueda)
        resultados["Eliminación"].append(eliminacion)

        print(
            f"{n:10d} | {insercion:15.6f} | "
            f"{busqueda:15.6f} | {eliminacion:15.6f}"
        )

if __name__ == "__main__":
    main()