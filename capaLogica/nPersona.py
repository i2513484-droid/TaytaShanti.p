# capaLogica/nPersona.py
from capaDatos.dPersona import DPersona

class NPersona:
    def __init__(self):
        self.datos = DPersona()
    
    # MÉTODO QUE PROBABLEMENTE FALTA EN TU CÓDIGO
    def obtener_todas_personas(self):
        """Obtiene todas las personas"""
        return self.datos.obtener_todos()
    
    def obtener_persona(self, doc_identidad):
        """Obtiene una persona específica"""
        return self.datos.obtener_por_documento(doc_identidad)
    
    def crear_persona(self, datos):
        """Crea una nueva persona"""
        return self.datos.crear(datos)
    
    def actualizar_personas(self, datos, doc_identidad):
        """Actualiza una persona"""
        return self.datos.actualizar(doc_identidad, datos)
    
    def eliminar_persona(self, doc_identidad):
        """Elimina una persona"""
        return self.datos.eliminar(doc_identidad)
