# capaDatos/dPersona.py
from conexion import conexion_db
from typing import List, Optional, Dict, Any

class DPersona:
    def __init__(self, table_name: str = 'personas'):
        """
        Inicializa el acceso a datos para personas.
        
        Args:
            table_name: Nombre de la tabla en Supabase (por defecto 'personas')
        """
        try:
            self.supabase = conexion_db.get_client()
            self.table_name = table_name
            print(f"✅ DPersona inicializado para tabla '{table_name}'")
        except Exception as e:
            raise ConnectionError(f"No se pudo inicializar DPersona: {e}")
    
    @property
    def table(self):
        """Propiedad que retorna la tabla de Supabase"""
        return self.supabase.table(self.table_name)
    
    def actualizar(self, doc_identidad: str, datos: dict) -> Optional[Dict]:
        """
        Actualiza una persona por documento de identidad.
        
        Args:
            doc_identidad: Documento de identidad de la persona
            datos: Diccionario con los datos a actualizar
            
        Returns:
            Diccionario con los datos actualizados o None si no se encontró
            
        Raises:
            ValueError: Si no se encuentra la persona
            Exception: Para otros errores
        """
        try:
            if not doc_identidad or not str(doc_identidad).strip():
                raise ValueError("El documento de identidad no puede estar vacío")
            
            if not datos or not isinstance(datos, dict):
                raise ValueError("Los datos para actualizar no son válidos")
            
            response = self.table.update(datos).eq('docIdentidad', doc_identidad).execute()
            
            if not response.data:
                raise ValueError(f"No se encontró persona con documento: {doc_identidad}")
            
            print(f"✅ Persona con documento {doc_identidad} actualizada exitosamente")
            return response.data[0]
            
        except ValueError as ve:
            # Relanzar errores de validación
            raise ve
        except Exception as e:
            raise Exception(f"Error al actualizar persona {doc_identidad}: {str(e)}")
    
    def obtener_todos(self) -> List[Dict]:
        """Obtiene todas las personas ordenadas por nombre"""
        try:
            response = self.table.select("*").order('nombre').execute()
            return response.data
        except Exception as e:
            raise Exception(f"Error al obtener todas las personas: {str(e)}")
    
    def obtener_por_documento(self, doc_identidad: str) -> Optional[Dict]:
        """Obtiene una persona específica por documento de identidad"""
        try:
            response = self.table.select("*").eq('docIdentidad', doc_identidad).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            raise Exception(f"Error al obtener persona {doc_identidad}: {str(e)}")
    
    def crear(self, datos: dict) -> Dict:
        """Crea una nueva persona"""
        try:
            campos_requeridos = ['docIdentidad', 'nombre', 'apellido']
            for campo in campos_requeridos:
                if campo not in datos or not str(datos[campo]).strip():
                    raise ValueError(f"Campo requerido faltante o vacío: {campo}")
            
            existente = self.obtener_por_documento(datos['docIdentidad'])
            if existente:
                raise ValueError(f"Ya existe una persona con documento {datos['docIdentidad']}")
            response = self.table.insert(datos).execute()
            
            if not response.data:
                raise Exception("No se pudo crear la persona")
        
            print(f"✅ Persona creada exitosamente: {datos['docIdentidad']}")
            return response.data[0]
            
        except ValueError as ve:
            raise ve
        except Exception as e:
            raise Exception(f"Error al crear persona: {str(e)}")
    
    def eliminar(self, doc_identidad: str) -> Optional[Dict]:
        """Elimina una persona por documento de identidad"""
        try:
            persona = self.obtener_por_documento(doc_identidad)
            if not persona:
                raise ValueError(f"No existe persona con documento {doc_identidad}")
            
            response = self.table.delete().eq('docIdentidad', doc_identidad).execute()
            
            print(f"✅ Persona eliminada exitosamente: {doc_identidad}")
            return persona
            
        except ValueError as ve:
            raise ve
        except Exception as e:
            raise Exception(f"Error al eliminar persona {doc_identidad}: {str(e)}")
