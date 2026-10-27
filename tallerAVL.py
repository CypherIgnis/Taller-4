class Nodo:

    def __init__(self, clave: int):
        self.clave: int = clave
        self.izquierdo: Nodo | None = None
        self.derecho: Nodo | None = None
        self.altura: int = 1


class ArbolAVL:

    def __init__(self):
        self.raiz: Nodo | None = None

    def obtener_altura(self, nodo: Nodo | None) -> int:
        if nodo is None:
            return 0
        return nodo.altura

    def actualizar_altura(self, nodo: Nodo) -> None:
        nodo.altura = 1 + max(
            self.obtener_altura(nodo.izquierdo),
            self.obtener_altura(nodo.derecho),
        )

    def factor_equilibrio(self, nodo: Nodo | None) -> int:
        if nodo is None:
            return 0

        return (
            self.obtener_altura(nodo.izquierdo)
            - self.obtener_altura(nodo.derecho)
        )

    def rotar_derecha(self, y: Nodo) -> Nodo:
        x = y.izquierdo
        subarbol = x.derecho

        x.derecho = y
        y.izquierdo = subarbol

        self.actualizar_altura(y)
        self.actualizar_altura(x)

        return x

    def rotar_izquierda(self, x: Nodo) -> Nodo:
        y = x.derecho
        subarbol = y.izquierdo

        y.izquierdo = x
        x.derecho = subarbol

        self.actualizar_altura(x)
        self.actualizar_altura(y)

        return y


    def insertar(self, clave: int) -> None:
        self.raiz = self._insertar(self.raiz, clave)

    def _insertar(
        self, nodo: Nodo | None, clave: int
    ) -> Nodo:
        if nodo is None:
            return Nodo(clave)

        if clave < nodo.clave:
            nodo.izquierdo = self._insertar(nodo.izquierdo, clave)
        elif clave > nodo.clave:
            nodo.derecho = self._insertar(nodo.derecho, clave)
        else:
            return nodo

        self.actualizar_altura(nodo)

        balance = self.factor_equilibrio(nodo)

        if balance > 1 and clave < nodo.izquierdo.clave:
            return self.rotar_derecha(nodo)

        if balance < -1 and clave > nodo.derecho.clave:
            return self.rotar_izquierda(nodo)

        if balance > 1 and clave > nodo.izquierdo.clave:
            nodo.izquierdo = self.rotar_izquierda(nodo.izquierdo)
            return self.rotar_derecha(nodo)

        if balance < -1 and clave < nodo.derecho.clave:
            nodo.derecho = self.rotar_derecha(nodo.derecho)
            return self.rotar_izquierda(nodo)

        return nodo

    def buscar(self, clave: int) -> bool:
        actual = self.raiz

        while actual is not None:
            if clave == actual.clave:
                return True
            elif clave < actual.clave:
                actual = actual.izquierdo
            else:
                actual = actual.derecho

        return False

    def eliminar(self, clave: int) -> bool:
        self.raiz, eliminada = self._eliminar(self.raiz, clave)
        return eliminada

    def _eliminar(
        self, nodo: Nodo | None, clave: int
    ) -> tuple[Nodo | None, bool]:
        if nodo is None:
            return None, False

        eliminada = False

        if clave < nodo.clave:
            nodo.izquierdo, eliminada = self._eliminar(
                nodo.izquierdo, clave
            )
        elif clave > nodo.clave:
            nodo.derecho, eliminada = self._eliminar(
                nodo.derecho, clave
            )
        else:
            eliminada = True

            if nodo.izquierdo is None and nodo.derecho is None:
                return None, True

            if nodo.izquierdo is None:
                return nodo.derecho, True

            if nodo.derecho is None:
                return nodo.izquierdo, True

            sucesor = nodo.derecho
            while sucesor.izquierdo is not None:
                sucesor = sucesor.izquierdo

            nodo.clave = sucesor.clave
            nodo.derecho, _ = self._eliminar(
                nodo.derecho, sucesor.clave
            )

        if not eliminada:
            return nodo, False

        self.actualizar_altura(nodo)

        balance = self.factor_equilibrio(nodo)

        if balance > 1 and self.factor_equilibrio(nodo.izquierdo) >= 0:
            return self.rotar_derecha(nodo), True

        if balance > 1 and self.factor_equilibrio(nodo.izquierdo) < 0:
            nodo.izquierdo = self.rotar_izquierda(nodo.izquierdo)
            return self.rotar_derecha(nodo), True

        if balance < -1 and self.factor_equilibrio(nodo.derecho) <= 0:
            return self.rotar_izquierda(nodo), True

        if balance < -1 and self.factor_equilibrio(nodo.derecho) > 0:
            nodo.derecho = self.rotar_derecha(nodo.derecho)
            return self.rotar_izquierda(nodo), True

        return nodo, True


    def inorden(self) -> list[int]:
        resultado: list[int] = []
        self._inorden(self.raiz, resultado)
        return resultado

    def _inorden(
        self, nodo: Nodo | None, resultado: list[int]
    ) -> None:
        if nodo is None:
            return

        self._inorden(nodo.izquierdo, resultado)
        resultado.append(nodo.clave)
        self._inorden(nodo.derecho, resultado)


    def altura(self) -> int:
        return self.obtener_altura(self.raiz)

    def cantidad_nodos(self) -> int:
        return self._contar_nodos(self.raiz)

    def _contar_nodos(self, nodo: Nodo | None) -> int:
        if nodo is None:
            return 0

        return (
            1
            + self._contar_nodos(nodo.izquierdo)
            + self._contar_nodos(nodo.derecho)
        )

    def validar(self) -> bool:
        _, _, correcto = self._validar(self.raiz, None, None)
        return correcto

    def _validar(
        self,
        nodo: Nodo | None,
        minimo: int | None,
        maximo: int | None,
    ) -> tuple[int, int, bool]:
        if nodo is None:
            return 0, 0, True

        if minimo is not None and nodo.clave <= minimo:
            return 0, 0, False

        if maximo is not None and nodo.clave >= maximo:
            return 0, 0, False

        altura_izq, cantidad_izq, correcto_izq = self._validar(
            nodo.izquierdo, minimo, nodo.clave
        )

        altura_der, cantidad_der, correcto_der = self._validar(
            nodo.derecho, nodo.clave, maximo
        )

        altura_real = 1 + max(altura_izq, altura_der)
        balance = altura_izq - altura_der

        correcto = (
            correcto_izq
            and correcto_der
            and abs(balance) <= 1
            and nodo.altura == altura_real
        )

        return (
            altura_real,
            cantidad_izq + cantidad_der + 1,
            correcto,
        )

#Demo

if __name__ == "__main__":
    arbol = ArbolAVL()

    claves = [30, 20, 10, 25, 40, 50, 22]

    for clave in claves:
        arbol.insertar(clave)

    print("Claves ordenadas:", arbol.inorden())
    print("Altura:", arbol.altura())
    print("Cantidad de nodos:", arbol.cantidad_nodos())
    print("¿Existe la clave 25?:", arbol.buscar(25))
    print("¿Existe la clave 99?:", arbol.buscar(99))
    print("¿Árbol válido?:", arbol.validar())

    print("¿Se eliminó la clave 20?:", arbol.eliminar(20))
    print("Claves después de eliminar:", arbol.inorden())
    print("¿Árbol válido después de eliminar?:", arbol.validar())


