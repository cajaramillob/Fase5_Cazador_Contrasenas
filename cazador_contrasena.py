"""Autor: Carlos Andres Jaramillo Britto
Ingenieria de Sistemas
Universidad Nacional Abierta y a Distancia
Vicerrectoría Académica y de Investigación
Curso: Programación
Código: 213023
Fase 5 Entrega proyecto de software"""

# importar librerías necesarias
import random
import string  # esta trabaja con cadenas de texto, números y caracteres especiales

# 1. EXCEPCIONES PERSONALIZADAS


class ErrorJuego(Exception):
    """Clase base para los errores del juego."""

    pass


class LongitudInvalidaError(ErrorJuego):
    """Se genera cuando la longitud no cumple los requisitos."""

    pass


class DatoNoNumericoError(ErrorJuego):
    """Se genera cuando el usuario ingresa un dato no numérico."""

    pass


class ContrasenaInvalidaError(ErrorJuego):
    """Se genera cuando una contraseña no cumple los requisitos."""

    pass


# 2. CLASE CONTRASENA


class Contrasena:
    """
    Se encarga de generar contraseñas aleatorias
    y comprobar si cumplen los requisitos del juego.
    """

    # Caracteres especiales permitidos por la guía.
    ESPECIALES = "¿¡?=)(/¨*+-%&$#!."

    def __init__(self, longitud):
        """
        Constructor de la clase.
        Recibe la longitud solicitada por el jugador.
        """

        # Comprobar que el dato sea numérico.
        if isinstance(longitud, bool) or not isinstance(longitud, int):
            raise DatoNoNumericoError("La longitud debe ser un número entero.")

        # Comprobar la longitud mínima.
        if longitud < 8:
            raise LongitudInvalidaError("La contraseña debe tener mínimo 8 caracteres.")

        # Guardar la longitud mediante encapsulamiento.
        self.__longitud = longitud

        # Inicialmente no existe una contraseña generada.
        self.__valor = ""

    def generar(self):
        """
        Genera una contraseña utilizando caracteres aleatorios.
        No garantiza que todos los requisitos se cumplan.
        """

        # Obtener las letras mayúsculas.
        mayusculas = string.ascii_uppercase

        # Obtener las letras minúsculas.
        minusculas = string.ascii_lowercase

        # Obtener los números.
        numeros = string.digits

        # Obtener los caracteres especiales.
        especiales = self.ESPECIALES

        # Unir todos los caracteres disponibles.
        caracteres = mayusculas + minusculas + numeros + especiales

        # Comprobar que existan suficientes caracteres únicos.
        if self.__longitud > len(set(caracteres)):
            raise LongitudInvalidaError(
                "La longitud supera la cantidad de " "caracteres únicos disponibles."
            )

        # Seleccionar caracteres sin repetir.
        seleccion = random.sample(list(set(caracteres)), self.__longitud)

        # Mezclar el orden de los caracteres.
        random.shuffle(seleccion)

        # Convertir la lista en una cadena de texto.
        self.__valor = "".join(seleccion)

        return self.__valor

    def validar(self):
        """
        Comprueba que la contraseña cumpla todos los requisitos.
        """

        # Verificar que exista una contraseña.
        if not self.__valor:
            raise ContrasenaInvalidaError("Primero debes generar una contraseña.")

        # Verificar la longitud mínima.
        if len(self.__valor) < 8:
            raise ContrasenaInvalidaError("La contraseña tiene menos de 8 caracteres.")

        # Verificar que exista una letra mayúscula.
        if not any(c.isupper() for c in self.__valor):
            raise ContrasenaInvalidaError("Falta al menos una letra mayúscula.")

        # Verificar que exista una letra minúscula.
        if not any(c.islower() for c in self.__valor):
            raise ContrasenaInvalidaError("Falta al menos una letra minúscula.")

        # Verificar que exista un número.
        if not any(c.isdigit() for c in self.__valor):
            raise ContrasenaInvalidaError("Falta al menos un número.")

        # Verificar que exista un carácter especial permitido.
        if not any(c in self.ESPECIALES for c in self.__valor):
            raise ContrasenaInvalidaError("Falta un carácter especial.")

        # Verificar que no existan caracteres repetidos.
        if len(set(self.__valor)) != len(self.__valor):
            raise ContrasenaInvalidaError(
                "La contraseña contiene caracteres repetidos."
            )

        return True


# ============================================================
# PRUEBA TEMPORAL DE LA CLASE CONTRASENA
# ============================================================

try:

    # Crear un objeto con longitud de 8 caracteres.
    prueba = Contrasena(8)

    # Generar una contraseña.
    resultado = prueba.generar()

    print("\nCONTRASEÑA GENERADA:")
    print(resultado)

    # Intentar validar la contraseña.
    if prueba.validar():
        print("Resultado: CONTRASEÑA VÁLIDA.")

except ContrasenaInvalidaError as error:

    print("Resultado: CONTRASEÑA INVÁLIDA.")
    print("Motivo:", error)

except ErrorJuego as error:

    print("Error:", error)
