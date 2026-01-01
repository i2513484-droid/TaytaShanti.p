# capaDatos/dPersona.py
from conexion import conexion_db

class DPersona:  # ← ¡Asegúrate que se llama DPersona, NO DPersonal!
    def __init__(self):
        self.supabase = conexion_db.get_client()
        self.table_name = 'personas'
    
    @property
    def table(self):
        return self.supabase.table(self.table_name)
    
    # MÉTODO INSERTAR (no existe, debe llamarse CREAR)
    def insertar(self, datos: dict):  # ← Si usas 'insertar' en tu código
        """Alias para crear - para mantener compatibilidad"""
        return self.crear(datos)
    
    def crear(self, datos: dict):
        """Crea una nueva persona"""
        try:
            response = self.table.insert(datos).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            raise Exception(f"Error al crear persona: {str(e)}")
    
    def obtener_todos(self):
        """Obtiene todas las personas"""
        try:
            response = self.table.select("*").execute()
            return response.data
        except Exception as e:
            raise Exception(f"Error al obtener personas: {str(e)}")
    
    def actualizar(self, doc_identidad: str, datos: dict):
        """Actualiza una persona"""
        try:
            response = self.table.update(datos).eq('docIdentidad', doc_identidad).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            raise Exception(f"Error en actualizar: {str(e)}")
    
    def eliminar(self, doc_identidad: str):
        """Elimina una persona"""
        try:
            response = self.table.delete().eq('docIdentidad', doc_identidad).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            raise Exception(f"Error al eliminar persona: {str(e)}")
