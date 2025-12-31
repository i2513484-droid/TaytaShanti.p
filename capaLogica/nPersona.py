from capaDatos.dPersona import DPersona

class NPersona:
    def __init__(self):
        self.__dPersona = DPersona()

    # MÉTODO CORREGIDO - 2 PARÁMETROS
    def actualizarPersonas(self, persona: dict, docidentidad_original: str):
        """Actualiza una persona existente"""
        try:
            # Actualizar en la base de datos
            return self.__dPersona.actualizar(persona, docidentidad_original)
        except Exception as e:
            raise Exception(f"Error al actualizar persona: {e}")

    # Los otros métodos se mantienen igual
    def nuevaPersona(self, persona: dict):
        """Registra una nueva persona"""
        try:
            return self.__dPersona.insertar(persona)
        except Exception as e:
            raise Exception(f"Error al registrar persona: {e}")

    def mostrarPersonas(self):
        """Obtiene todas las personas"""
        try:
            return self.__dPersona.mostrar()
        except Exception as e:
            raise Exception(f"Error al obtener personas: {e}")

    def eliminarPersona(self, docidentidad: str):
        """Elimina una persona por documento de identidad"""
        try:
            return self.__dPersona.eliminar(docidentidad)
        except Exception as e:
            raise Exception(f"Error al eliminar persona: {e}")
