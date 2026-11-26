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
from abc import ABC, abstractmethod  # para crear clases abstractas

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


# 3. CLASE ABSTRACTA --> COFRE
class Cofre(ABC):
    """
    Clase abstracta que representa la estructura general
    de los cofres del juego.
    """

    def __init__(self, nombre, recompensa):
        """Inicializa el nombre y los puntos del cofre."""

        # Encapsular los atributos del cofre.
        self.__nombre = nombre
        self.__recompensa = recompensa

    @property
    def nombre(self):
        """Permite consultar el nombre del cofre."""
        return self.__nombre

    @property
    def recompensa(self):
        """Permite consultar los puntos del cofre."""
        return self.__recompensa

    @abstractmethod
    def obtener_recompensa(self):
        """
        Método abstracto que deberán implementar
        los diferentes tipos de cofres.
        """
        pass


# 4. TIPOS DE COFRES
class CofreComun(Cofre):
    """Representa el cofre común que entrega 10 puntos."""

    def __init__(self):
        super().__init__("Común", 10)

    def obtener_recompensa(self):
        return self.recompensa


class CofreRaro(Cofre):
    """Representa el cofre raro que entrega 25 puntos."""

    def __init__(self):
        super().__init__("Raro", 25)

    def obtener_recompensa(self):
        return self.recompensa


class CofreLegendario(Cofre):
    """Representa el cofre legendario que entrega 50 puntos."""

    def __init__(self):
        super().__init__("Legendario", 50)

    def obtener_recompensa(self):
        return self.recompensa


class CofreMaldito(Cofre):
    """Representa el cofre maldito que descuenta 20 puntos."""

    def __init__(self):
        super().__init__("Maldito", -20)

    def obtener_recompensa(self):
        return self.recompensa


# 5. CLASE JUEGOCAZADOR


class JuegoCazador:
    """
    Administra la puntuación y el funcionamiento
    general del juego Cazador de Contraseñas.
    """

    def __init__(self):
        """Inicializa una partida con cero puntos."""

        # Puntuación inicial del jugador.
        self.__puntos = 0

    @property
    def puntos(self):
        """Permite consultar la puntuación acumulada."""
        return self.__puntos

    def actualizar_puntuacion(self, cofre):
        # Suma o resta los puntos según el cofre obtenido.
        # Obtener la recompensa del cofre.
        puntos_obtenidos = cofre.obtener_recompensa()

        # Actualizar la puntuación acumulada.
        self.__puntos += puntos_obtenidos

        return self.__puntos

    def seleccionar_cofre(self, contrasena_valida):
        # Selecciona un cofre según el resultado de la validación de la contraseña.
        # Si la contraseña es válida, elegir un cofre positivo.
        if contrasena_valida:
            cofres_disponibles = [CofreComun(), CofreRaro(), CofreLegendario()]

            return random.choice(cofres_disponibles)

        # Si la contraseña es inválida, asignar el cofre maldito.
        return CofreMaldito()

    def jugar_ronda(self, longitud):
        """
        Ejecuta una ronda del juego:
        genera, valida y asigna un cofre.
        """

        # Crear el objeto contraseña.
        contrasena = Contrasena(longitud)

        # Generar la contraseña aleatoria.
        valor_generado = contrasena.generar()

        print("\nCONTRASEÑA GENERADA:")
        print(valor_generado)

        # Intentar validar la contraseña.
        try:
            contrasena_valida = contrasena.validar()

        except ContrasenaInvalidaError as error:
            contrasena_valida = False
            print("CONTRASEÑA INVÁLIDA.")
            print("Motivo:", error)

        else:
            print("CONTRASEÑA VÁLIDA.")

        # Seleccionar el cofre correspondiente.
        cofre = self.seleccionar_cofre(contrasena_valida)

        # Actualizar la puntuación.
        puntuacion = self.actualizar_puntuacion(cofre)

        # Mostrar el resultado de la ronda.
        print("\nCOFRE OBTENIDO:", cofre.nombre)
        print("Recompensa:", cofre.obtener_recompensa(), "puntos")
        print("Puntuación acumulada:", puntuacion, "puntos")


# 6. FUNCION PARA SOLICITAR LA LONGITUD


def solicitar_longitud():
    """
    Solicita la longitud de la contraseña.
    Repite la solicitud hasta recibir un dato válido.
    """

    while True:
        try:
            entrada = input("\nIngresa la longitud de la contraseña: ")

            # Convertir el texto ingresado a número entero.
            try:
                longitud = int(entrada)
            except ValueError:
                raise DatoNoNumericoError("Debes ingresar un número entero.")

            # Comprobar la longitud mínima.
            if longitud < 8:
                raise LongitudInvalidaError(
                    "La contraseña debe tener mínimo 8 caracteres."
                )

            # Calcular la cantidad máxima de caracteres únicos.
            caracteres = (
                string.ascii_uppercase
                + string.ascii_lowercase
                + string.digits
                + Contrasena.ESPECIALES
            )

            maximo = len(set(caracteres))

            if longitud > maximo:
                raise LongitudInvalidaError(
                    f"La longitud máxima permitida es {maximo}."
                )

            # Si todo está correcto, devolver la longitud.
            return longitud

        except (DatoNoNumericoError, LongitudInvalidaError) as error:
            print("\n¡Cuidado, cazador!")
            print("Entrada incorrecta:", error)
            print("Inténtalo nuevamente.")


print("\nPRUEBA DE SOLICITUD DE LONGITUD")

longitud_prueba = solicitar_longitud()

print("Longitud aceptada:", longitud_prueba)

# ============================================================
# PRUEBA TEMPORAL DE LOS CUATRO COFRES
# ============================================================

cofres = [CofreComun(), CofreRaro(), CofreLegendario(), CofreMaldito()]

print("\nPRUEBA DE LOS COFRES")

for cofre in cofres:
    print(
        "Cofre:",
        cofre.nombre,
        "| Recompensa:",
        str(cofre.obtener_recompensa()) + " puntos",
    )

# ============================================================
# PRUEBA TEMPORAL DEL COFRE COMUN
# ============================================================
cofre = CofreComun()

print("\nPRUEBA DEL COFRE COMUN")
print("Nombre:", cofre.nombre)
print("Recompensa:", cofre.obtener_recompensa())
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
# ============================================================
# PRUEBA TEMPORAL DE LA CLASE JUEGOCAZADOR
# ============================================================

juego = JuegoCazador()

print("\nPRUEBA DE PUNTUACIÓN")

print("Puntuación inicial:", juego.puntos, "puntos")

# Aplicar la recompensa del cofre maldito.
cofre = CofreMaldito()
resultado = juego.actualizar_puntuacion(cofre)

print("Después del cofre maldito:", resultado, "puntos")

# Aplicar la recompensa del cofre legendario.
cofre = CofreLegendario()
resultado = juego.actualizar_puntuacion(cofre)

print("Después del cofre legendario:", resultado, "puntos")


# ============================================================
# PRUEBA DE SELECCIÓN ALEATORIA DE COFRES
# ============================================================

juego = JuegoCazador()

print("\nPRUEBA DE SELECCIÓN DE COFRES")

# Simular una contraseña válida.
cofre = juego.seleccionar_cofre(True)
print(
    "Contraseña válida:",
    cofre.nombre,
    "| Recompensa:",
    cofre.obtener_recompensa(),
    "puntos",
)

# Simular una contraseña inválida.
cofre = juego.seleccionar_cofre(False)
print(
    "Contraseña inválida:",
    cofre.nombre,
    "| Recompensa:",
    cofre.obtener_recompensa(),
    "puntos",
)


# ==========================================
# PRUEBA DE UNA RONDA INTEGRADA
# ==========================================

print("\nPRUEBA DE UNA RONDA INTEGRADA")

# Crear una instancia del juego.
juego = JuegoCazador()

# Ejecutar una ronda con una contraseña de 8 caracteres.
juego.jugar_ronda(8)
