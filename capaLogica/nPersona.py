# capaLogica/nPersona.py
from capaDatos.dPersona import DPersona

class NPersona:
    def __init__(self):
        self.datos = DPersona()
    
    def obtener_todas_personas(self):
        """Obtiene todas las personas"""
        return self.datos.obtener_todos()
    
    def obtener_persona(self, doc_identidad: str):
        """Obtiene una persona por documento"""
        return self.datos.obtener_por_documento(doc_identidad)
    
    def crear_persona(self, datos: dict):
        """Crea una nueva persona con validaciones de negocio"""
        # Validaciones adicionales de negocio
        if 'edad' in datos and datos['edad']:
            if datos['edad'] < 18:
                raise ValueError("La persona debe ser mayor de edad")
        
        # Validar formato de email si existe
        if 'email' in datos and datos['email']:
            if '@' not in datos['email']:
                raise ValueError("Email no válido")
        
        return self.datos.crear(datos)
    
    def actualizar_personas(self, datos: dict, doc_identidad: str):
        """Actualiza una persona con validaciones de negocio"""
        # Validaciones adicionales
        if 'edad' in datos and datos['edad']:
            if datos['edad'] > 120:
                raise ValueError("Edad no válida")
        
        return self.datos.actualizar(doc_identidad, datos)
    
    def eliminar_persona(self, doc_identidad: str):
        """Elimina una persona"""
        return self.datos.eliminar(doc_identidad)
