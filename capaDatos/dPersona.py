from conexion import conexion_db
class DPersona:
    def __init__(self):
        self.supabase = conexion_db.get_client()
        self.table_name = 'personas'  # Cambia esto por tu tabla real
    
    @property
    def table(self):
        return self.supabase.table(self.table_name)
    
    def actualizar(self, doc_identidad: str, datos: dict):
        """Actualiza una persona por documento de identidad"""
        try:
            response = self.table.update(datos).eq('docIdentidad', doc_identidad).execute()
            
            if not response.data:
                raise ValueError(f"No se encontró persona con documento {doc_identidad}")
                
            return response.data[0]
        except Exception as e:
            raise Exception(f"Error en actualizar: {str(e)}")
    
    def obtener_todos(self):
        """Obtiene todas las personas"""
        try:
            response = self.table.select("*").execute()
            return response.data
        except Exception as e:
            raise Exception(f"Error al obtener personas: {str(e)}")
    
    def crear(self, datos: dict):
        """Crea una nueva persona"""
        try:
            response = self.table.insert(datos).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            raise Exception(f"Error al crear persona: {str(e)}")
    
    def eliminar(self, doc_identidad: str):
        """Elimina una persona por documento de identidad"""
        try:
            response = self.table.delete().eq('docIdentidad', doc_identidad).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            raise Exception(f"Error al eliminar persona: {str(e)}")
